import { Pool } from "pg";
import { config } from "../../config";
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { email: email, number: number } = req.body;
  const queries = [
    // "DROP TABLE IF EXISTS users;",
    "CREATE TABLE IF NOT EXISTS users (email VARCHAR(20) PRIMARY KEY, number VARCHAR(12) NOT NULL);",
    `UPSERT INTO users (email, number) VALUES ('${email}', '${number}');`,
    "SELECT * FROM users;",
  ];

  try {
    const pool = new Pool(config);
    const client = await pool.connect();

    for (let i = 0; i < queries.length; i++) {
      let result = await client.query(queries[i]);
      if (result.rows) {
        result.rows.forEach((row) => {
          console.log(row.message);
        });
      }
    }
    // await client.end();

    res.status(200).json({ message: "Success!" });
  } catch (err: any) {
    res.status(500).json({
      message: err.message,
    });
  }
}
