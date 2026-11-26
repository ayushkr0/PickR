import type { Metadata, Viewport } from "next";
import Script from "next/script";
import Providers from "@/components/Providers";
import "./globals.css";

export const viewport: Viewport = {
  viewportFit: "cover",
};

export const metadata: Metadata = {
  title: "PickR — AI Product Recommendations",
  description:
    "Smart product recommendations powered by AI. Find the perfect laptop, headphones, or camera in seconds.",
};

// Novus by Pendo install snippet plus the one-time anonymous initialize call.
const PENDO_SNIPPET = `(function(apiKey){
    (function(p,e,n,d,o){var v,w,x,y,z;o=p[d]=p[d]||{};o._q=o._q||[];
    v=['initialize','identify','updateOptions','pageLoad','track', 'trackAgent'];for(w=0,x=v.length;w<x;++w)(function(m){
    o[m]=o[m]||function(){o._q[m===v[0]?'unshift':'push']([m].concat([].slice.call(arguments,0)));};})(v[w]);
    y=e.createElement(n);y.async=!0;y.src='https://cdn.pendo.io/agent/static/'+apiKey+'/pendo.js';
    z=e.getElementsByTagName(n)[0];z.parentNode.insertBefore(y,z);})(window,document,'script','pendo');
})('0baac2a1-cf90-4f34-adad-f254d4333529');

// Boot Pendo once per page load with an anonymous visitor. The signed-in
// visitor is registered later with pendo.identify() in src/lib/auth.tsx.
pendo.initialize({
  visitor: {
    id: ''
  }
});`;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <body className="h-dvh flex flex-col">
        <Script id="pendo-install" strategy="beforeInteractive">
          {PENDO_SNIPPET}
        </Script>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
