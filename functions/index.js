import * as latestCommitHandler from './api/latest-commit.js';

export const onRequest = async (context) => {
  try {
    const url = new URL(context.request.url);
    if (url.pathname.startsWith('/api/latest-commit')) {
      return latestCommitHandler.onRequest(context);
    }
    if (typeof context.next === 'function') {
      return context.next();
    }
    return new Response('Not found', { status: 404 });
  } catch (error) {
    console.error('Function error', error);
    return new Response('Internal server error', { status: 500 });
  }
};

export default {
  onRequest,
};
