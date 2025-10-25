import { Nunito } from "next/font/google";
import type { Metadata } from "next";
import "./globals.css";
import ThemeToggle from "@/components/ThemeToggle";

const nunito = Nunito({
    subsets: ["latin"],
    variable: "--font-nunito",
});

export const metadata: Metadata = {
    title: "Peter's Bookstore",
    description: "I write about thoughts, stories, and ideas.",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={nunito.className} style={{ background: 'var(--background-color)', color: 'var(--text-color)' }}>
                <div className="max-w-4xl mx-auto min-h-3xl flex flex-col" style={{ background: 'var(--background-color)' }}>
                    <header>
                        <div className="max-w-4xl mx-auto px-4 py-6 flex items-center justify-between">
                            <a href="/" className="text-2xl font-bold transition-colors" style={{ color: 'var(--text-color)' }}>
                                Peter's Bookstore
                            </a>
                            <ThemeToggle />
                        </div>
                    </header>
                    <main className="max-w-4xl px-4 py-8 flex-grow">
                        {children}
                    </main>
                    <footer>
                        <div className="max-w-4xl mx-auto px-4 py-6 text-center" style={{ color: 'var(--text-color)', opacity: 0.8 }}>
                            <p>© {new Date().getFullYear()} Peter's Bookstore. All rights reserved.</p>
                        </div>
                    </footer>
                </div>
            </body>
        </html>
    );
}
