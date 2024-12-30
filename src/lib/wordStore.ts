import { writable } from 'svelte/store';
import { supabase } from '$lib/supabase';

export async function clearWordsFound(numberOfRows: number) {
	const { error } = await supabase
		.from('rows-' + numberOfRows)
		.delete()
		.neq('found', true);

	if (error) return console.log(error);
}

export const wordsFoundWritable = writable();

function updateWordFound(data: { found: boolean }[]) {
	wordsFoundWritable.set(data.map((word: { found: boolean }) => word.found));
}

export async function getWordsFound(numberOfRows: number) {
	const { data, error } = await supabase.from('rows-' + numberOfRows).select('*');

	if (error) {
		return console.log(error);
	}

	// idfk why i need to sort but the first index goes to the end
	data.sort((a, b) => a.id - b.id);

	updateWordFound(data);
}

export async function updateToFull(curNumWords: number, numOfWords: number, numberOfRows: number) {
	if (curNumWords >= numOfWords) return;

	const newData = [];
	for (let i = curNumWords; i < numOfWords; i++) {
		newData.push({ id: curNumWords + i, found: false });
	}
	const { error } = await supabase.from('rows-' + numberOfRows).insert(newData);

	if (error) {
		return console.log(error);
	}

	getWordsFound(numberOfRows);
}

export async function foundWordUpdate(id: number, numberOfRows: number) {
	const { error } = await supabase
		.from('rows-' + numberOfRows)
		.update({ found: true })
		.eq('id', id);

	if (error) {
		return console.log(error);
	}

	getWordsFound(numberOfRows);
}
