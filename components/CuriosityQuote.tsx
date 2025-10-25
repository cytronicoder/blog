'use client';

import { useEffect, useState } from 'react';

interface Quote {
    q: string;
    a: string;
    h: string;
}

export default function CuriosityQuote() {
    const [quote, setQuote] = useState<Quote | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchQuote = async () => {
            try {
                setLoading(true);
                const response = await fetch('/api/quote');
                if (!response.ok) {
                    throw new Error('Failed to fetch quote');
                }
                const data = await response.json();
                setQuote(data[0]);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to fetch quote');
            } finally {
                setLoading(false);
            }
        };

        fetchQuote();
    }, []);

    if (loading) {
        return (
            <div className="text-center py-8">
                <div className="animate-pulse">
                    <div className="h-4 bg-gray-300 rounded w-3/4 mx-auto mb-2"></div>
                    <div className="h-3 bg-gray-300 rounded w-1/2 mx-auto"></div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center py-8">
                <p className="text-red-500">Failed to load quote: {error}</p>
            </div>
        );
    }

    if (!quote) {
        return null;
    }

    return (
        <div>
            <blockquote className="text-lg italic mb-4" style={{ color: 'var(--text-color)', opacity: 0.5 }}>
                "{quote.q}"
            </blockquote>
            <cite className="text-sm font-medium" style={{ color: 'var(--primary-color)' }}>
                — {quote.a}
            </cite>
        </div>
    );
}
