const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { ...CORS, 'Content-Type': 'application/json' } });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });

    const url = new URL(request.url);
    const kv = env.AI_ANALYST_REQUESTS;

    // ── Claude: GET /pending — list pending report requests ──
    if (request.method === 'GET') {
      const list = await kv.list({ prefix: 'request:' });
      const items = [];
      for (const key of list.keys) {
        const val = await kv.get(key.name);
        if (val) items.push({ id: key.name, ...JSON.parse(val) });
      }
      // Clean up old pending requests (older than 2 hours)
      const cutoff = Date.now() - 2 * 60 * 60 * 1000;
      for (const item of items) {
        if (new Date(item.createdAt).getTime() < cutoff) {
          await kv.delete(item.id);
        }
      }
      return json({ pending: items.filter(i => i.status === 'pending') });
    }

    // ── Claude: DELETE /?id=<key> — mark request as done ──
    if (request.method === 'DELETE') {
      const id = url.searchParams.get('id');
      if (!id) return json({ error: 'missing id' }, 400);
      await kv.delete(id);
      return json({ ok: true });
    }

    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405);

    // ── User: POST — submit a report request ──
    try {
      const { company } = await request.json();
      if (!company || typeof company !== 'string' || company.trim().length === 0) {
        return json({ error: '请输入公司名称' }, 400);
      }
      if (company.length > 200) {
        return json({ error: '公司名称过长' }, 400);
      }

      const name = company.trim();
      const id = `request:${Date.now()}:${Math.random().toString(36).slice(2, 8)}`;
      const entry = { company: name, status: 'pending', createdAt: new Date().toISOString() };
      await kv.put(id, JSON.stringify(entry));

      return json({ ok: true, message: `「${name}」已提交，Claude 即将生成报告`, id });
    } catch (e) {
      return json({ error: e.message || '请求失败' }, 500);
    }
  },
};
