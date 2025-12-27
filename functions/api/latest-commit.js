const GITHUB_API = 'https://api.github.com/repos';

const jsonResponse = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

const buildPayload = (commit) => {
  const {
    sha,
    html_url: url,
    commit: {
      message,
      author: { name: author = 'Unknown', date = '' } = {},
    } = {},
  } = commit;

  return { sha, url, message, author, date };
};

const getCommit = async (repo, env) => {
  if (!repo) {
    return jsonResponse({ error: 'repo parameter required' }, 400);
  }

  const result = await fetch(`${GITHUB_API}/${repo}/commits`, {
    headers: {
      Accept: 'application/vnd.github+json',
      ...(env.GITHUB_TOKEN && { Authorization: `Bearer ${env.GITHUB_TOKEN}` }),
    },
  });

  if (!result.ok) {
    const text = await result.text();
    return new Response(text, { status: result.status });
  }

  const commits = await result.json();
  if (!Array.isArray(commits) || commits.length === 0) {
    return jsonResponse({ error: 'no commits found' }, 404);
  }

  return jsonResponse(buildPayload(commits[0]));
};

export async function onRequest(context) {
  const repo = context.request.url ? new URL(context.request.url).searchParams.get('repo') : null;
  return getCommit(repo, context.env);
}
