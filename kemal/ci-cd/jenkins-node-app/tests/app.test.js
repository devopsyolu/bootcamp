// test/app.test.js
const request = require('supertest');
const app = require('../src/app');

describe('GET /', () => {
  it('should return the correct text', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toEqual(200);
    expect(res.text).toContain("Bu urun Jenkins uzerinde CI calistirilarak olusturulmustur, devopsyolu.");
  });
});
