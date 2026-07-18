import { defineConfig } from "astro/config";

// Static site. Set `site` to your final domain for correct canonical URLs and sitemap.
export default defineConfig({
  site: "https://readthemasters.example",
  build: { format: "directory" },
});
