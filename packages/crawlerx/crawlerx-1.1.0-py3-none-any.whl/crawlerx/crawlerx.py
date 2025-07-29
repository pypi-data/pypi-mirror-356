import argparse
import os
import json
import threading
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs, urljoin, urldefrag
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
import re
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pickle

def is_valid_url(url, headers, session):
    try:
        result = session.head(url, timeout=args.timeout, headers=headers)
        return result.status_code < 400
    except requests.RequestException:
        return False

def get_domain(url):
    parsed = urlparse(url)
    return parsed.netloc.replace('www.', '')

def create_output_directory(base_url, output_dir):
    domain = get_domain(base_url)
    folder_name = f"crawlerx_{domain}"
    output_path = os.path.join(output_dir, folder_name)
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(output_path, 'get'), exist_ok=True)
    os.makedirs(os.path.join(output_path, 'post'), exist_ok=True)
    os.makedirs(os.path.join(output_path, 'dir'), exist_ok=True)
    os.makedirs(os.path.join(output_path, 'files'), exist_ok=True)
    if args.structure:
        os.makedirs(os.path.join(output_path, 'structure'), exist_ok=True)
    return output_path

def write_urls(urls, output_path, method='get'):
    filename_txt = os.path.join(output_path, method, f"{method}_requests.txt")
    filename_json = os.path.join(output_path, method, f"{method}_requests.json")
    with open(filename_txt, 'w', encoding='utf-8') as f:
        for url in sorted(urls):
            f.write(f"{url}\n")
    with open(filename_json, 'w', encoding='utf-8') as f:
        json.dump(list(urls), f, indent=2)

def write_post_requests(post_data, output_path):
    filename_txt = os.path.join(output_path, 'post', 'post_requests.txt')
    filename_json = os.path.join(output_path, 'post', 'post_requests.json')
    with open(filename_txt, 'w', encoding='utf-8') as f:
        for data in post_data:
            f.write(f"URL: {data['url']}\n")
            f.write(f"Parameters: {data['params']}\n")
            f.write("//===//\n")
    with open(filename_json, 'w', encoding='utf-8') as f:
        json.dump(post_data, f, indent=2)

def write_structure_tree(tree_data, output_path=None):
    def build_ascii_tree(urls, base_netloc):
        if not urls:
            return "No URLs found to build site structure."
        tree = {}
        for url in sorted(urls):
            parsed = urlparse(url)
            netloc = parsed.netloc
            path = parsed.path or '/'
            if parsed.query:
                path += f"?{parsed.query}"
            components = [netloc] + [comp for comp in path.split('/') if comp]
            current = tree
            for i, comp in enumerate(components):
                if comp not in current:
                    current[comp] = {'__url__': url, '__children__': {}}
                current = current[comp]['__children__']
        def render_tree(node, prefix="", depth=0):
            lines = []
            keys = sorted([k for k in node.keys() if k != '__children__' and k != '__url__'])
            for i, key in enumerate(keys):
                is_last = i == len(keys) - 1
                line_prefix = prefix + ("└── " if is_last else "├── ")
                lines.append(f"{line_prefix}{key} ({node[key]['__url__']})")
                child_lines = render_tree(node[key]['__children__'], prefix + ("    " if is_last else "│   "), depth + 1)
                lines.extend(child_lines)
            return lines
        return "\n".join([f"Site Structure for {base_netloc}:"] + render_tree(tree))
    
    base_netloc = urlparse(next(iter(tree_data), '')).netloc if tree_data else "unknown"
    ascii_tree = build_ascii_tree(tree_data, base_netloc)
    if output_path:
        filename = os.path.join(output_path, 'structure', 'structure.txt')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(ascii_tree)
    return ascii_tree

def write_directories_and_files(urls, output_path):
    directories = set()
    files = set()
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path
        if not parsed.query and path and path != '/':
            components = [comp for comp in path.split('/') if comp]
            if len(components) > 1:
                dir_path = '/'.join(components[:-1])
                directories.add(f"{parsed.scheme}://{parsed.netloc}/{dir_path}/")
            if '.' in components[-1]:
                files.add(url)
    with open(os.path.join(output_path, 'dir', 'dirs.txt'), 'w', encoding='utf-8') as f:
        for dir_url in sorted(directories):
            f.write(f"{dir_url}\n")
    with open(os.path.join(output_path, 'files', 'files.txt'), 'w', encoding='utf-8') as f:
        for file_url in sorted(files):
            f.write(f"{file_url}\n")

def write_resources(resource_urls, output_path):
    categorized = {'images': set(), 'scripts': set(), 'css': set(), 'other': set()}
    for resource_type, url in resource_urls:
        if resource_type == 'image':
            categorized['images'].add(url)
        elif resource_type == 'script':
            categorized['scripts'].add(url)
        elif resource_type == 'css':
            categorized['css'].add(url)
        else:
            categorized['other'].add(url)
    for category, urls in categorized.items():
        if urls:
            filename_txt = os.path.join(output_path, 'files', f"{category}.txt")
            filename_json = os.path.join(output_path, 'files', f"{category}.json")
            with open(filename_txt, 'w', encoding='utf-8') as f:
                for url in sorted(urls):
                    f.write(f"{url}\n")
            with open(filename_json, 'w', encoding='utf-8') as f:
                json.dump(list(urls), f, indent=2)

def can_fetch(url, user_agent, headers, session):
    rp = RobotFileParser()
    try:
        robots_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt"
        response = session.get(robots_url, timeout=args.timeout, headers=headers)
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except requests.RequestException:
        return True

def should_exclude(url, exclude_extensions):
    exclude_extensions = exclude_extensions.split(',')
    return any(url.lower().endswith(f'.{ext.strip()}') for ext in exclude_extensions)

def is_within_domain(url, base_url):
    base_netloc = urlparse(base_url).netloc
    url_netloc = urlparse(url).netloc
    if args.sub:
        return base_netloc in url_netloc or url_netloc.endswith(f".{base_netloc}")
    return base_netloc == url_netloc

def extract_urls(soup, base_url):
    urls = set()
    tag_attributes = [
        ('a', ['href']),
        ('link', ['href']),
        ('form', ['action']),
        ('img', ['src', 'data-src']),
        ('script', ['src']),
        ('iframe', ['src']),
        ('video', ['src', 'poster']),
        ('audio', ['src']),
        ('source', ['src', 'srcset']),
        ('button', ['formaction']),
        ('object', ['data']),
        ('embed', ['src']),
        ('meta', ['content']),
        ('*', ['data-url', 'data-href']),
    ]
    for tag_name, attrs in tag_attributes:
        for tag in soup.find_all(tag_name):
            for attr in attrs:
                url = tag.get(attr)
                if url:
                    try:
                        if tag_name == 'meta' and attr == 'content':
                            if 'url=' in url.lower():
                                url = re.search(r'url=(.*?)(?:$|;|\s)', url, re.I).group(1)
                            else:
                                continue
                        full_url = urljoin(base_url, url.strip())
                        full_url = urldefrag(full_url)[0]
                        if is_within_domain(full_url, base_url) and not should_exclude(full_url, args.exclude):
                            urls.add(full_url)
                    except (ValueError, AttributeError):
                        pass
    urls.update(extract_inline_urls(soup, base_url))
    for tag in soup.find_all(True):
        for attr in tag.attrs:
            if attr.startswith('on') or attr in ['style', 'data-url']:
                value = tag.get(attr)
                if value:
                    extracted_urls = extract_urls_from_text(value, base_url)
                    urls.update(extracted_urls)
    return urls

def extract_inline_urls(soup, base_url):
    urls = set()
    for tag in soup.find_all(['script', 'style']):
        if not tag.get('src') and tag.string:
            extracted_urls = extract_urls_from_text(tag.string, base_url)
            urls.update(extracted_urls)
    return urls

def extract_urls_from_text(text, base_url):
    urls = set()
    url_pattern = r'(?:(?:https?://|//)[^\s"\'<>)]+|(?:/|[.]{1,2}/)[^\s"\'<>)]+|[^\s"\'<>)]+\.(?:jpg|jpeg|png|gif|js|css|svg|woff2?|ttf|eot|pdf|mp4|mp3))'
    matches = re.findall(url_pattern, text, re.I)
    for match in matches:
        try:
            full_url = urljoin(base_url, match.strip())
            full_url = urldefrag(full_url)[0]
            if is_within_domain(full_url, base_url) and not should_exclude(full_url, args.exclude):
                urls.add(full_url)
        except ValueError:
            pass
    return urls

def extract_css_urls(response, base_url):
    urls = set()
    css_content = response.text
    url_pattern = r'url\([\'"]?(.*?)[\'"]?\)'
    matches = re.findall(url_pattern, css_content, re.I)
    for match in matches:
        try:
            full_url = urljoin(base_url, match.strip())
            full_url = urldefrag(full_url)[0]
            if is_within_domain(full_url, base_url) and not should_exclude(full_url, args.exclude):
                urls.add(full_url)
        except ValueError:
            pass
    return urls

def extract_post_data(soup, base_url):
    post_requests = []
    for form in soup.find_all('form', method=re.compile(r'post', re.I)):
        action = form.get('action')
        full_url = urljoin(base_url, action) if action else base_url
        if is_within_domain(full_url, base_url):
            inputs = form.find_all(['input', 'textarea', 'select'])
            params = {}
            for inp in inputs:
                name = inp.get('name')
                if name:
                    value = inp.get('value') or ''
                    params[name] = value
            if params:
                post_requests.append({'url': full_url, 'params': params})
    return post_requests

def parse_headers(header_string):
    headers = {}
    if not header_string:
        return headers
    try:
        for header in header_string.split(';'):
            header = header.strip()
            if not header:
                continue
            if ':' not in header:
                print(f"Invalid header format: {header}. Expected 'key: value'.", flush=True)
                continue
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error parsing headers: {e}", flush=True)
    return headers

def crawl_url(current_url, current_depth, session, visited, get_urls, post_data, to_visit, lock, skipped_urls, resource_urls):
    if current_depth > args.depth:
        return
    with lock:
        if current_url in visited or not is_valid_url(current_url, session.headers, session):
            return
        visited.add(current_url)
    if not can_fetch(current_url, args.ua, session.headers, session):
        print(f"[!] {current_url} blocked by robots.txt", flush=True)
        return
    print(f"[*] Crawling: {current_url} (Depth: {current_depth})", flush=True)
    try:
        response = session.get(current_url, timeout=args.timeout)
        if response.status_code != 200:
            print(f"[!] Non-200 response for {current_url}: {response.status_code}", flush=True)
            return
        if current_url.lower().endswith('.css'):
            css_urls = extract_css_urls(response, current_url)
            with lock:
                for css_url in css_urls:
                    resource_urls.add(('css_resource', css_url))
                    print(f"[CSS Resource] {css_url}", flush=True)
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = extract_urls(soup, current_url)
        new_urls = []
        for new_url in urls:
            with lock:
                if new_url not in visited:
                    has_params = bool(parse_qs(urlparse(new_url).query))
                    resource_type = 'other'
                    if any(new_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']):
                        resource_type = 'image'
                    elif new_url.lower().endswith('.js'):
                        resource_type = 'script'
                    elif new_url.lower().endswith('.css'):
                        resource_type = 'css'
                    if has_params:
                        get_urls.add(new_url)
                        print(f"[GET] {new_url}", flush=True)
                    else:
                        skipped_urls.add(new_url)
                        print(f"[SKIPPED] {new_url} (No query parameters)", flush=True)
                    resource_urls.add((resource_type, new_url))
                    print(f"[{resource_type.capitalize()}] {new_url}", flush=True)
                    if current_depth + 1 <= args.depth:
                        new_urls.append((new_url, current_depth + 1))
        with lock:
            to_visit.extend(new_urls)
        post_requests = extract_post_data(soup, current_url)
        with lock:
            for req in post_requests:
                post_data.append(req)
                print(f"[POST] URL: {req['url']}", flush=True)
                print(f"[POST] Parameters: {req['params']}", flush=True)
                print("//===//", flush=True)
        time.sleep(args.delay)
    except requests.RequestException as e:
        print(f"[!] Request failed for {current_url}: {e}", flush=True)
    except Exception as e:
        print(f"[!] Unexpected error for {current_url}: {e}", flush=True)

def crawl(url):
    visited = set()
    to_visit = [(url, 0)]
    get_urls = set()
    post_data = []
    skipped_urls = set()
    resource_urls = set()
    lock = threading.Lock()
    if args.cont:
        try:
            with open(args.cont, 'rb') as f:
                state = pickle.load(f)
                visited = state.get('visited', set())
                get_urls = state.get('get_urls', set())
                post_data = state.get('post_data', [])
                to_visit = state.get('to_visit', [(url, 0)])
                resource_urls = state.get('resource_urls', set())
                print(f"[*] Resumed crawl from {args.cont}", flush=True)
        except Exception as e:
            print(f"[!] Failed to load crawl state: {e}", flush=True)
    session = requests.Session()
    session.headers.update({'User-Agent': args.ua})
    if args.headers:
        session.headers.update(parse_headers(args.headers))
    if args.proxy:
        session.proxies.update(args.proxy)
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = []
            processed_urls = set()
            while to_visit:
                with lock:
                    current_batch = [(u, d) for u, d in to_visit if u not in processed_urls]
                    to_visit = [(u, d) for u, d in to_visit if u in processed_urls]
                if not current_batch:
                    break
                for current_url, current_depth in current_batch:
                    with lock:
                        if current_url in visited or current_url in processed_urls:
                            continue
                        processed_urls.add(current_url)
                    future = executor.submit(
                        crawl_url,
                        current_url,
                        current_depth,
                        session,
                        visited,
                        get_urls,
                        post_data,
                        to_visit,
                        lock,
                        skipped_urls,
                        resource_urls
                    )
                    futures.append(future)
                for future in futures:
                    try:
                        future.result()
                    except Exception:
                        pass
                futures = []
                time.sleep(0.01)
        if args.output:
            state = {
                'visited': visited,
                'get_urls': get_urls,
                'post_data': post_data,
                'to_visit': to_visit,
                'resource_urls': resource_urls
            }
            with open(os.path.join(args.output, f"crawlerx_{get_domain(url)}", 'crawl_state.pkl'), 'wb') as f:
                pickle.dump(state, f)
    except KeyboardInterrupt:
        print("\n[!] Crawling stopped by user (Ctrl+C).", flush=True)
        if args.output:
            state = {
                'visited': visited,
                'get_urls': get_urls,
                'post_data': post_data,
                'to_visit': to_visit,
                'resource_urls': resource_urls
            }
            with open(os.path.join(args.output, f"crawlerx_{get_domain(url)}", 'crawl_state.pkl'), 'wb') as f:
                pickle.dump(state, f)
            print(f"[*] Crawl state saved to {os.path.join(args.output, f'crawlerx_{get_domain(url)}', 'crawl_state.pkl')}", flush=True)
        executor._threads.clear()
    if skipped_urls:
        print(f"\n[*] Skipped {len(skipped_urls)} URLs due to no query parameters:", flush=True)
        for url in sorted(skipped_urls):
            print(f"[SKIPPED] {url}", flush=True)
    return get_urls, post_data, resource_urls

def main():
    ascii_logo = r"""
	 ▄▄· ▄▄▄   ▄▄▄· ▄▄▌ ▐ ▄▌▄▄▌  ▄▄▄ .▄▄▄  ▐▄• ▄ 
	▐█ ▌▪▀▄ █·▐█ ▀█ ██· █▌▐███•  ▀▄.▀·▀▄ █· █▌█▌▪	            ╦╔╦╗╔═╗┌─┐┬ ┬┬─┐┌┐ ┌─┐
	██ ▄▄▐▀▀▄ ▄█▀▀█ ██▪▐█▐▐▌██▪  ▐▀▀▪▄▐▀▀▄  ·██·     AUTHOR:    ║║║║╠═╣├─┘│ │├┬┘├┴┐│ │
	▐███▌▐█•█▌▐█ ▪▐▌▐█▌██▐█▌▐█▌▐▌▐█▄▄▌▐█•█▌▪▐█·█▌	            ╩╩ ╩╩ ╩┴  └─┘┴└─└─┘└─┘
	·▀▀▀ .▀  ▀ ▀  ▀  ▀▀▀▀ ▀▪.▀▀▀  ▀▀▀ .▀  ▀•▀▀ ▀▀
                                          
        CrawlerX - The Ultimate Web Crawler
    """
    print(ascii_logo)
    parser = argparse.ArgumentParser(description="CrawlerX - The Ultimate Web Crawler")
    parser.add_argument('-u', '--url', required=True, help="Target URL to crawl (e.g., https://example.com)")
    parser.add_argument('-o', '--output', default=None, help="Output directory (default: None, prints to terminal)")
    parser.add_argument('--structure', action='store_true', help="Generate ASCII site structure")
    parser.add_argument('-H', '--headers', default=None, help="Custom headers (e.g., 'Cookie: session=abc; Authorization: Bearer xyz')")
    parser.add_argument('--threads', type=int, default=1, help="Number of concurrent threads (default: 1, max: 20)")
    parser.add_argument('--depth', type=int, default=3, help="Maximum crawling depth (default: 3)")
    parser.add_argument('--ua', default='CrawlerX/1.0', help="Custom User-Agent string")
    parser.add_argument('--exclude', default='jpg,jpeg,png,gif,pdf,css,js', help="Comma-separated file extensions to exclude")
    parser.add_argument('--sub', action='store_true', help="Include subdomains in crawling")
    parser.add_argument('--proxy', default=None, help="Proxy server (e.g., http://proxy:port)")
    parser.add_argument('--timeout', type=int, default=5, help="Request timeout in seconds (default: 5)")
    parser.add_argument('--delay', type=float, default=1.0, help="Delay between requests in seconds (default: 1.0)")
    parser.add_argument('--cont', default=None, help="Path to crawl state pickle file to resume crawling")
    global args
    args = parser.parse_args()
    args.threads = max(1, min(args.threads, 20))
    print(f"[*] Using {args.threads} threads", flush=True)
    if not args.url.startswith(('http://', 'https://')):
        args.url = f"https://{args.url}"
        print(f"[*] Prepended https:// to URL: {args.url}", flush=True)
    args.proxy = {'http': args.proxy, 'https': args.proxy} if args.proxy else None
    if args.headers:
        headers = parse_headers(args.headers)
        if not headers:
            print("Invalid or empty headers provided. Continuing without custom headers.", flush=True)
        else:
            print(f"[*] Using custom headers: {headers}", flush=True)
    session = requests.Session()
    if not is_valid_url(args.url, parse_headers(args.headers), session):
        print("Invalid URL or site is unreachable.", flush=True)
        return
    output_path = None
    if args.output:
        output_path = create_output_directory(args.url, args.output)
    print(f"[*] Starting crawl for {args.url} (Depth: {args.depth})", flush=True)
    try:
        get_urls, post_data, resource_urls = crawl(args.url)
    except Exception as e:
        print(f"[!] Crawling failed: {e}", flush=True)
        get_urls, post_data, resource_urls = set(), [], set()
    if args.output and get_urls:
        write_urls(get_urls, output_path, 'get')
        print(f"[*] Saved {len(get_urls)} GET URLs with query parameters to {output_path}/get/", flush=True)
        write_directories_and_files(get_urls, output_path)
        print(f"[*] Saved directories and files to {output_path}/dir/ and {output_path}/files/", flush=True)
        if resource_urls:
            write_resources(resource_urls, output_path)
            print(f"[*] Saved categorized resources to {output_path}/files/", flush=True)
    elif get_urls:
        print(f"[*] Found {len(get_urls)} GET URLs with query parameters.", flush=True)
    if args.output and post_data:
        write_post_requests(post_data, output_path)
        print(f"[*] Saved {len(post_data)} POST requests to {output_path}/post/", flush=True)
    elif post_data:
        print(f"[*] Found {len(post_data)} POST requests.", flush=True)
    if args.structure:
        ascii_tree = write_structure_tree(get_urls, output_path if args.output else None)
        if not args.output:
            if ascii_tree.startswith("No URLs"):
                print(f"\n[*] {ascii_tree}", flush=True)
            else:
                print("\n[*] Site Structure:", flush=True)
                print(ascii_tree, flush=True)
        elif get_urls:
            print(f"[*] Site structure saved to {output_path}/structure/structure.txt", flush=True)
        else:
            print("\n[*] No URLs found to build site structure.", flush=True)
    if args.output:
        print(f"[*] Crawling complete. Results saved in {output_path}", flush=True)
    else:
        print(f"[*] Crawling complete. Found: {len(get_urls)} GET URLs, {len(post_data)} POST requests, {len(resource_urls)} resources.", flush=True)

if __name__ == "__main__":
    main()
