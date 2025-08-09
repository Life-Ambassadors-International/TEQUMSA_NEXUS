import { Router } from 'express';

const router = Router();

// POST /broadcast route to handle lattice broadcast
router.post('/broadcast', (req, res) => {
  const { topic, payload, phi7777 } = req.body;
  // TODO: integrate with lattice broadcasting service
  res.json({ status: 'broadcast received', topic, phi7777 });
});

// GET /echo route for health check or echo
router.get('/echo', (req, res) => {
  res.json({ message: 'echo from lattice routes' });
});

export default router;
