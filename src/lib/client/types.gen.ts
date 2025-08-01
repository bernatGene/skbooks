// This file is auto-generated by @hey-api/openapi-ts

/**
 * ValidationError
 */
export type ValidationError = {
	/**
	 * Location
	 */
	loc: Array<string | number>;
	/**
	 * Message
	 */
	msg: string;
	/**
	 * Error Type
	 */
	type: string;
};

/**
 * ShelfReadWithBookCount
 */
export type ShelfReadWithBookCount = {
	/**
	 * Number
	 */
	number: number;
	/**
	 * Bookcase Id
	 */
	bookcase_id?: number | null;
	/**
	 * Id
	 */
	id: number;
	/**
	 * Book Count
	 */
	book_count: number;
};

/**
 * ShelfRead
 */
export type ShelfRead = {
	/**
	 * Number
	 */
	number: number;
	/**
	 * Bookcase Id
	 */
	bookcase_id?: number | null;
	/**
	 * Id
	 */
	id: number;
};

/**
 * PublisherRead
 */
export type PublisherRead = {
	/**
	 * Name
	 */
	name: string;
	/**
	 * Id
	 */
	id: number;
	/**
	 * Aliases
	 */
	aliases?: Array<string>;
};

/**
 * HTTPValidationError
 */
export type HttpValidationError = {
	/**
	 * Detail
	 */
	detail?: Array<ValidationError>;
};

/**
 * CategoryRead
 */
export type CategoryRead = {
	/**
	 * Name
	 */
	name: string;
	/**
	 * Id
	 */
	id: number;
};

/**
 * BookcaseReadWithCounts
 */
export type BookcaseReadWithCounts = {
	/**
	 * Name
	 */
	name: string;
	/**
	 * Id
	 */
	id: number;
	/**
	 * Shelves
	 */
	shelves?: Array<ShelfReadWithBookCount>;
};

/**
 * BookUpdate
 */
export type BookUpdate = {
	/**
	 * Title
	 */
	title?: string | null;
	/**
	 * Subtitle
	 */
	subtitle?: string | null;
	/**
	 * Isbn 13
	 */
	isbn_13?: string | null;
	/**
	 * Isbn 10
	 */
	isbn_10?: string | null;
	/**
	 * Published Date
	 */
	published_date?: string | null;
	/**
	 * Page Count
	 */
	page_count?: number | null;
	/**
	 * Language
	 */
	language?: string | null;
	/**
	 * Description
	 */
	description?: string | null;
	/**
	 * Image Link
	 */
	image_link?: string | null;
	/**
	 * Shelf Id
	 */
	shelf_id?: number | null;
	/**
	 * Publisher Id
	 */
	publisher_id?: number | null;
	/**
	 * Authors
	 */
	authors?: Array<string> | null;
	/**
	 * Translators
	 */
	translators?: Array<string> | null;
	/**
	 * Categories
	 */
	categories?: Array<string> | null;
	/**
	 * Is Translation
	 */
	is_translation?: boolean | null;
	/**
	 * Original Language
	 */
	original_language?: string | null;
	/**
	 * Translation Language
	 */
	translation_language?: string | null;
};

/**
 * BookReadWithDetails
 */
export type BookReadWithDetails = {
	/**
	 * Title
	 */
	title: string;
	/**
	 * Subtitle
	 */
	subtitle?: string | null;
	/**
	 * Isbn 13
	 */
	isbn_13: string;
	/**
	 * Isbn 10
	 */
	isbn_10?: string | null;
	/**
	 * Published Date
	 */
	published_date?: string | null;
	/**
	 * Page Count
	 */
	page_count?: number | null;
	/**
	 * Language
	 */
	language?: string | null;
	/**
	 * Description
	 */
	description?: string | null;
	/**
	 * Image Link
	 */
	image_link?: string | null;
	/**
	 * Is Translation
	 */
	is_translation?: boolean;
	/**
	 * Original Language
	 */
	original_language?: string | null;
	/**
	 * Translation Language
	 */
	translation_language?: string | null;
	/**
	 * Shelf Id
	 */
	shelf_id?: number | null;
	/**
	 * Publisher Id
	 */
	publisher_id?: number | null;
	/**
	 * Id
	 */
	id: number;
	/**
	 * Authors
	 */
	authors?: Array<AuthorRead>;
	/**
	 * Translators
	 */
	translators?: Array<AuthorRead>;
	/**
	 * Categories
	 */
	categories?: Array<CategoryRead>;
	shelf?: ShelfRead | null;
	publisher?: PublisherRead | null;
};

/**
 * AuthorRead
 */
export type AuthorRead = {
	/**
	 * Name
	 */
	name: string;
	/**
	 * Id
	 */
	id: number;
};

/**
 * BookRead
 */
export type BookRead = {
	/**
	 * Title
	 */
	title: string;
	/**
	 * Subtitle
	 */
	subtitle?: string | null;
	/**
	 * Isbn 13
	 */
	isbn_13: string;
	/**
	 * Isbn 10
	 */
	isbn_10?: string | null;
	/**
	 * Published Date
	 */
	published_date?: string | null;
	/**
	 * Page Count
	 */
	page_count?: number | null;
	/**
	 * Language
	 */
	language?: string | null;
	/**
	 * Description
	 */
	description?: string | null;
	/**
	 * Image Link
	 */
	image_link?: string | null;
	/**
	 * Is Translation
	 */
	is_translation?: boolean;
	/**
	 * Original Language
	 */
	original_language?: string | null;
	/**
	 * Translation Language
	 */
	translation_language?: string | null;
	/**
	 * Shelf Id
	 */
	shelf_id?: number | null;
	/**
	 * Publisher Id
	 */
	publisher_id?: number | null;
	/**
	 * Id
	 */
	id: number;
};

/**
 * BookInfo
 */
export type BookInfo = {
	/**
	 * Title
	 */
	title: string;
	/**
	 * Authors
	 */
	authors: Array<string>;
	/**
	 * Publisher
	 */
	publisher?: string | null;
	/**
	 * Published Date
	 */
	published_date?: string | null;
	/**
	 * Thumbnail
	 */
	thumbnail?: string | null;
	/**
	 * Identifier
	 */
	identifier: string;
	/**
	 * Is Translation
	 */
	is_translation?: boolean;
	/**
	 * Translators
	 */
	translators?: Array<string>;
	/**
	 * Original Language
	 */
	original_language?: string | null;
	/**
	 * Translation Language
	 */
	translation_language?: string | null;
};

/**
 * BookCreate
 */
export type BookCreate = {
	/**
	 * Title
	 */
	title: string;
	/**
	 * Subtitle
	 */
	subtitle?: string | null;
	/**
	 * Isbn 13
	 */
	isbn_13: string;
	/**
	 * Isbn 10
	 */
	isbn_10?: string | null;
	/**
	 * Published Date
	 */
	published_date?: string | null;
	/**
	 * Page Count
	 */
	page_count?: number | null;
	/**
	 * Language
	 */
	language?: string | null;
	/**
	 * Description
	 */
	description?: string | null;
	/**
	 * Image Link
	 */
	image_link?: string | null;
	/**
	 * Is Translation
	 */
	is_translation?: boolean;
	/**
	 * Original Language
	 */
	original_language?: string | null;
	/**
	 * Translation Language
	 */
	translation_language?: string | null;
	/**
	 * Shelf Id
	 */
	shelf_id?: number | null;
	/**
	 * Publisher Id
	 */
	publisher_id?: number | null;
	/**
	 * Authors
	 */
	authors?: Array<string>;
	/**
	 * Translators
	 */
	translators?: Array<string>;
	/**
	 * Categories
	 */
	categories?: Array<string>;
	/**
	 * Publisher
	 */
	publisher?: string | null;
};

export type ReadBookcasesWithCountsGetData = {
	body?: never;
	path?: never;
	query?: never;
	url: '/api/bookcases/';
};

export type ReadBookcasesWithCountsGetResponses = {
	/**
	 * Response Read Bookcases With Counts Api Bookcases  Get
	 * Successful Response
	 */
	200: Array<BookcaseReadWithCounts>;
};

export type ReadBookcasesWithCountsGetResponse =
	ReadBookcasesWithCountsGetResponses[keyof ReadBookcasesWithCountsGetResponses];

export type ReadBooksGetData = {
	body?: never;
	path?: never;
	query?: {
		/**
		 * Offset
		 */
		offset?: number;
		/**
		 * Limit
		 */
		limit?: number;
	};
	url: '/api/books/';
};

export type ReadBooksGetErrors = {
	/**
	 * Validation Error
	 */
	422: HttpValidationError;
};

export type ReadBooksGetError = ReadBooksGetErrors[keyof ReadBooksGetErrors];

export type ReadBooksGetResponses = {
	/**
	 * Response Read Books Api Books  Get
	 * Successful Response
	 */
	200: Array<BookRead>;
};

export type ReadBooksGetResponse = ReadBooksGetResponses[keyof ReadBooksGetResponses];

export type CreateBookPostData = {
	body: BookCreate;
	path?: never;
	query?: never;
	url: '/api/books/';
};

export type CreateBookPostErrors = {
	/**
	 * Validation Error
	 */
	422: HttpValidationError;
};

export type CreateBookPostError = CreateBookPostErrors[keyof CreateBookPostErrors];

export type CreateBookPostResponses = {
	/**
	 * Successful Response
	 */
	200: BookReadWithDetails;
};

export type CreateBookPostResponse = CreateBookPostResponses[keyof CreateBookPostResponses];

export type DeleteBookDeleteData = {
	body?: never;
	path: {
		/**
		 * Book Id
		 */
		book_id: number;
	};
	query?: never;
	url: '/api/books/{book_id}';
};

export type DeleteBookDeleteErrors = {
	/**
	 * Validation Error
	 */
	422: HttpValidationError;
};

export type DeleteBookDeleteError = DeleteBookDeleteErrors[keyof DeleteBookDeleteErrors];

export type DeleteBookDeleteResponses = {
	/**
	 * Successful Response
	 */
	200: unknown;
};

export type ReadBookGetData = {
	body?: never;
	path: {
		/**
		 * Book Id
		 */
		book_id: number;
	};
	query?: never;
	url: '/api/books/{book_id}';
};

export type ReadBookGetErrors = {
	/**
	 * Validation Error
	 */
	422: HttpValidationError;
};

export type ReadBookGetError = ReadBookGetErrors[keyof ReadBookGetErrors];

export type ReadBookGetResponses = {
	/**
	 * Successful Response
	 */
	200: BookReadWithDetails;
};

export type ReadBookGetResponse = ReadBookGetResponses[keyof ReadBookGetResponses];

export type UpdateBookPatchData = {
	body: BookUpdate;
	path: {
		/**
		 * Book Id
		 */
		book_id: number;
	};
	query?: never;
	url: '/api/books/{book_id}';
};

export type UpdateBookPatchErrors = {
	/**
	 * Validation Error
	 */
	422: HttpValidationError;
};

export type UpdateBookPatchError = UpdateBookPatchErrors[keyof UpdateBookPatchErrors];

export type UpdateBookPatchResponses = {
	/**
	 * Successful Response
	 */
	200: BookReadWithDetails;
};

export type UpdateBookPatchResponse = UpdateBookPatchResponses[keyof UpdateBookPatchResponses];

export type GetBookByIsbnGetData = {
	body?: never;
	path: {
		/**
		 * Isbn
		 */
		isbn: string;
	};
	query?: never;
	url: '/api/isbn/{isbn}';
};

export type GetBookByIsbnGetErrors = {
	/**
	 * Validation Error
	 */
	422: HttpValidationError;
};

export type GetBookByIsbnGetError = GetBookByIsbnGetErrors[keyof GetBookByIsbnGetErrors];

export type GetBookByIsbnGetResponses = {
	/**
	 * Successful Response
	 */
	200: BookInfo;
};

export type GetBookByIsbnGetResponse = GetBookByIsbnGetResponses[keyof GetBookByIsbnGetResponses];

export type RootGetData = {
	body?: never;
	path?: never;
	query?: never;
	url: '/';
};

export type RootGetResponses = {
	/**
	 * Successful Response
	 */
	200: unknown;
};

export type ClientOptions = {
	baseUrl: 'http://localhost:8000' | (string & {});
};
