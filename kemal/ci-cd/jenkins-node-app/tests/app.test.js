const request = require('supertest');
const app = require('../src/app');

describe('GET /', () => {
    it('responds with Hello, Jenkins CI!', async () => {
        const res = await request(app).get('/');
        expect(res.statusCode).toBe(200);
        expect(res.text).toBe('Hello, Jenkins CI!');
    });
});
