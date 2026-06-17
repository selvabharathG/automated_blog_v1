import { defineConfig } from 'vitepress'
export default defineConfig({
  title: "Automated Research Blog",
  description: "AI/ML Latest Insights",
  base: '/automated_blog_v1/', 
  themeConfig: {
    nav: [{ text: 'Home', link: '/' }],
    sidebar: [{ text: 'Latest Research Posts', items: [{ text: 'Welcome to My Blog', link: '/' }] }]
  }
})