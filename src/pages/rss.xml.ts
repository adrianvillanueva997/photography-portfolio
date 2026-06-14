import rss from '@astrojs/rss';
import yaml from 'js-yaml';

interface Photo {
	id: string;
	title: string;
	image: string;
	metadata: {
		dateTaken: string;
		location: string;
		[key: string]: any;
	};
}

interface Collection {
	collection: string;
	description: string;
	photos: Photo[];
}

export async function GET() {
	const collectionFiles = import.meta.glob('../data/collections/*.yaml', {
		query: '?raw',
		import: 'default',
	});

	const items: Array<{ title: string; description: string; link: string; pubDate: Date }> = [];

	for (const [path, getContent] of Object.entries(collectionFiles)) {
		const content = (await getContent()) as string;
		const data = yaml.load(content) as Collection;
		const slug = path.split('/').pop()?.replace('.yaml', '') || '';
		const dateTaken = data.photos[0]?.metadata?.dateTaken;
		const parsedDate = dateTaken
			? new Date(dateTaken.replace(/(\d{4}):(\d{2}):(\d{2})/, '$1-$2-$3'))
			: new Date();

		items.push({
			title: data.collection,
			description: data.description || `${data.photos.length} photographs`,
			link: `/collections/${slug}/`,
			pubDate: parsedDate,
		});
	}

	items.sort((a, b) => b.pubDate.getTime() - a.pubDate.getTime());

	return rss({
		title: 'Adrian Villanueva - Photography Portfolio',
		description: 'New photography collections from Adrian Villanueva, Tokyo-based photographer.',
		site: 'https://avm.photography',
		items,
		customData: '<language>en</language>',
	});
}
