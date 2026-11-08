import type { Metadata, Viewport } from "next";
import { Fraunces, Nunito_Sans, IBM_Plex_Mono } from "next/font/google";
import { ThemeProvider } from "@/components/layout/ThemeProvider";
import { SiteHeader } from "@/components/layout/SiteHeader";
import { ServiceWorkerRegister } from "@/components/layout/ServiceWorkerRegister";
import "./globals.css";

const display = Nunito_Sans({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["400", "600", "700", "800"],
});

const displayAlt = Fraunces({
  variable: "--font-display-alt",
  subsets: ["latin"],
});

const mono = IBM_Plex_Mono({
  variable: "--font-code",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "NeetCode 150 Learn",
  description:
    "Kid-simple animated explanations of all NeetCode 150 problems for Google interview prep.",
  manifest: "/manifest.webmanifest",
  appleWebApp: {
    capable: true,
    title: "NC150 Learn",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f3f7f4" },
    { media: "(prefers-color-scheme: dark)", color: "#0b1411" },
  ],
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${display.variable} ${displayAlt.variable} ${mono.variable} antialiased`}
      >
        <ThemeProvider>
          <ServiceWorkerRegister />
          <SiteHeader />
          <main>{children}</main>
          <footer className="mx-auto max-w-6xl px-4 py-10 text-sm text-muted">
            NeetCode 150 Learn · offline-friendly study companion · not affiliated
            with NeetCode or LeetCode
          </footer>
        </ThemeProvider>
      </body>
    </html>
  );
}
