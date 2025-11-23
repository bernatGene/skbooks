import {
	createBookcasePost,
	createShelfPost,
	readBookcasesWithCountsGet
} from '$lib/client';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const { data } = await readBookcasesWithCountsGet();
	return { bookcases: data };
};

export const actions: Actions = {
	createBookcase: async () => {
		const { data: newBookcase } = await createBookcasePost({
			body: { name: 'New Bookcase' }
		});

		if (newBookcase) {
			await createShelfPost({
				body: {
					bookcase_id: newBookcase.id,
					number: 1
				}
			});
		}

		return { success: true };
	}
};
