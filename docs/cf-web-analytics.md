# Cloudflare Web Analytics

thefamilygems.com is hosted on GitHub Pages and is **not** proxied by Cloudflare, so the beacon is not injected for you. `build.py` adds it only when `data/cf-web-analytics.json` has `enabled` set to `true` and a non-empty `token`.

Ops and Joshua authorized $0 Cloudflare Web Analytics on October 23, 2026. Do not invent a token or page-view numbers. Control Center expects traffic source `familygem-site` with `cf_host: thefamilygems.com` once the Web Analytics site exists.

## Turn it on

1. In the Cloudflare dashboard, open Web Analytics for `thefamilygems.com` and copy the token from the JavaScript snippet (`data-cf-beacon` → `token`).
2. Edit `data/cf-web-analytics.json`: paste that token into `token`, set `enabled` to `true`, and leave `host` as `thefamilygems.com`.
3. Rebuild: `python3 build.py`
4. Check a built page (for example `index.html`) contains:

   ```html
   <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"YOUR_TOKEN"}'></script>
   ```

5. Commit the config and the rebuilt HTML, then push. GitHub Pages serves those files.

If `enabled` is false or `token` is empty, the rebuild omits the script on every page.

This site has no Content-Security-Policy. If one is added later, allow `https://static.cloudflareinsights.com` in `script-src` and `https://cloudflareinsights.com` in `connect-src` (same allowances as `websiteplz-site/build.py`).

Privacy copy lives in `page_privacy()` in `build.py`. It says the site uses Cloudflare Web Analytics, which counts page views without cookies and doesn't track you across other sites.
