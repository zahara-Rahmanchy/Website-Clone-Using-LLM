export async function CloneWebsite(url: string) {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/clone/advanced', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
      cache: 'no-store',
    });

    if (!res.ok) {
      throw new Error(await res.text());
    }

    const data = await res.json();
    return { html: data.cloned_html };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (err: any) {
    return { error: err.message || 'Unknown error' };
  }
}
