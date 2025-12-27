import * as latestCommitHandler from './api/latest-commit.js';

export const onRequest = async (context) => {
  const url = new URL(context.request.url);
  if (url.pathname.startsWith('/api/latest-commit')) {
    return latestCommitHandler.onRequest(context);
  }
  return new Response('Not found', { status: 404 });
};
