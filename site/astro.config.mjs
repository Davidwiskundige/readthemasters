import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Static site. `site` is the public canonical URL, used for the sitemap and canonical links.
// The Cloudflare Pages project also stays reachable at readthemasters.pages.dev.
export default defineConfig({
  site: "https://readthemasters.org",
  build: { format: "directory" },
  integrations: [sitemap()],
});
