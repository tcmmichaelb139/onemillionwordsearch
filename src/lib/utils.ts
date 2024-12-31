function distance(a: number[], b: number[]): number {
	return (
		Math.abs(a[0] - b[0]) * Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]) * Math.abs(a[1] - b[1])
	);
}

function optimalEnd(start: number[], cur: number[]): number[] {
	const [a, b] = start;
	const [c, d] = cur;
	const horVerDir = [
		[a, d],
		[c, b]
	];

	const directions = horVerDir.concat(
		Math.abs(c - a) < Math.abs(d - b)
			? [
					[a - Math.abs(b - d), d],
					[a + Math.abs(b - d), d]
				]
			: [
					[c, b - Math.abs(a - c)],
					[c, b + Math.abs(a - c)]
				]
	);

	return directions.reduce((a, b) => (distance(cur, a) < distance(cur, b) ? a : b));
}

function getSequnece(start: number[], end: number[]): { [key: string]: boolean } {
	const sequence: { [key: string]: boolean } = {};

	if (start[0] === end[0]) {
		if (start[1] > end[1]) [start, end] = [end, start];
		for (let i = start[1]; i <= end[1]; i++) {
			sequence[start[0] + '|' + i] = true;
		}
	} else if (start[1] === end[1]) {
		if (start[0] > end[0]) [start, end] = [end, start];
		for (let i = start[0]; i <= end[0]; i++) {
			sequence[i + '|' + start[1]] = true;
		}
	} else {
		if (start[0] > end[0]) [start, end] = [end, start];
		const slope = (end[1] - start[1]) / (end[0] - start[0]);

		for (let i = 0; i <= Math.abs(start[0] - end[0]); i++) {
			sequence[start[0] + i + '|' + (start[1] + i * slope)] = true;
		}
	}

	return sequence;
}

export function optimalWordSequence(start: number[], cur: number[]): { [key: string]: boolean } {
	const end = optimalEnd(start, cur);

	return getSequnece(start, end);
}

export function getAllWordsSequence(words: string[]): { [key: string]: number } {
	let sequence: { [key: string]: number } = {};

	for (let i = 0; i < words.length; i++) {
		const data = JSON.parse(words[i]);
		const seq = optimalWordSequence(data[0], data[1]);

		// merge sequence and seq objects but add the values if they are the same
		sequence = Object.keys(seq).reduce((a, b) => {
			a[b] = a[b] ? a[b] + 1 : 1;
			return a;
		}, sequence);
	}

	return sequence;
}
