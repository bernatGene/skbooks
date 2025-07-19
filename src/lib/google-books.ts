export interface BookInfo {
	title: string;
	authors: string[];
	publisher?: string;
	publishedDate?: string;
	thumbnail?: string;
	identifier: string;
}

const UNKNOWN_BOOK: BookInfo = {
	title: 'Unknown Title',
	authors: ['Unknown Author'],
	publisher: 'Unknown Publisher',
	publishedDate: 'Unknown Date',
	thumbnail: '/no-image-placeholder.svg',
	identifier: ''
};

export async function getBookInfoByISBN(isbn: string): Promise<BookInfo> {
	const apiKey = import.meta.env.VITE_API_KEY;
	if (!apiKey) {
		console.error('Google Books API key is missing. Please set VITE_API_KEY in your .env file.');
		return { ...UNKNOWN_BOOK, identifier: isbn, title: 'API Key Missing' };
	}

	const url = `https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}&key=${apiKey}`;

	try {
		const response = await fetch(url);
		if (!response.ok) {
			console.error(`Google Books API request failed with status: ${response.status}`);
			return { ...UNKNOWN_BOOK, identifier: isbn, title: 'API Request Failed' };
		}

		const data = await response.json();

		if (data.totalItems > 0 && data.items[0].volumeInfo) {
			const volumeInfo = data.items[0].volumeInfo;
			return {
				title: volumeInfo.title || UNKNOWN_BOOK.title,
				authors: volumeInfo.authors || UNKNOWN_BOOK.authors,
				publisher: volumeInfo.publisher || UNKNOWN_BOOK.publisher,
				publishedDate: volumeInfo.publishedDate || UNKNOWN_BOOK.publishedDate,
				thumbnail: volumeInfo.imageLinks?.thumbnail || UNKNOWN_BOOK.thumbnail,
				identifier: isbn
			};
		}
		return { ...UNKNOWN_BOOK, identifier: isbn, title: 'Book Not Found' };
	} catch (error) {
		console.error('Error fetching book info:', error);
		return { ...UNKNOWN_BOOK, identifier: isbn, title: 'Error Fetching Data' };
	}
}
