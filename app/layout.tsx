import Link from "next/link"
import "./globals.css"
import { Inter } from "next/font/google"
import { ThemeProvider } from "@/components/theme-provider"
import { Analytics } from "@/components/analytics"
import { ModeToggle } from "@/components/mode-toggle"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "peter's bookstore",
  description: "exploring the edges of the extraordinary",
  icons: {
    icon: "https://blog.cytronicoder.com/favicon.ico",
    apple: "https://blog.cytronicoder.com/apple-touch-icon.png",
  },
  manifest: "https://blog.cytronicoder.com/site.webmanifest",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://blog.cytronicoder.com",
    siteName: "peter's bookstore",
    title: "peter's bookstore",
    description: "exploring the edges of the extraordinary",
    images: "https://blog.cytronicoder.com/og-image.png",
  },
  twitter: {
    creator: "@cytronicoder",
    site: "@cytronicoder",
    card: "summary_large_image",
  },
}

interface RootLayoutProps {
  children: React.ReactNode
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body
        className={`antialiased min-h-screen bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-50 ${inter.className}`}
      >
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <div className="max-w-2xl mx-auto p-10">
            <header>
              <div className="flex items-center justify-between">
                <div className="block">
                  <Link href="/">
                    <h1 className="text-2xl font-bold">
                      peter&apos;s bookstore
                    </h1>
                  </Link>
                  <p>exploring the edges of the extraordinary</p>
                </div>
                <nav className="ml-auto space-x-6">
                  <Link href="https://cytronicoder.com" target="_blank">
                    Portfolio
                  </Link>
                </nav>
                <ModeToggle />
              </div>
            </header>
            <main>{children}</main>
            <footer className="mt-12 text-center text-sm">
              <hr className="my-4 border-[#ec3750]" />
              <p>
                Copyright &copy; {new Date().getFullYear()} by{" "}
                <Link href="https://cytronicoder.com" target="_blank">
                  Zeyu Yao
                </Link>
                .
              </p>
              <p>
                Code open-sourced on{" "}
                <Link href="https://github.com/cytronicoder/blog" target="_blank" className="text-[#ec3750]">
                  <code>GitHub</code>
                </Link>
                {" "}- go check it out!
              </p>
            </footer>
          </div>
          <Analytics />
        </ThemeProvider>
      </body>
    </html>
  )
}
