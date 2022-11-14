import { Pool } from "pg";
import { config } from "../../../config";
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const pool = new Pool(config);
  const { email } = req.query;
  const queries = [
    "CREATE TABLE IF NOT EXISTS users (email VARCHAR(20) PRIMARY KEY, number VARCHAR(12) NOT NULL);",
    `SELECT number FROM users WHERE email = '${email}';`,
  ];

  try {
    const client = await pool.connect();
    let number = "";
    for (let i = 0; i < queries.length; i++) {
      const result = await client.query(queries[i]);
      if (result.rows) {
        number = result.rows[0];
      }
    }
    res.status(200).json(number);
  } catch (err: any) {
    res.status(500).json({
      message: err.message,
    });
  }
}
