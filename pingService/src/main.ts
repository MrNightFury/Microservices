import express from "express"
import { env } from "node:process";

const application = express();

application.get("/", (_, res) => {
    res.status(200).send("Hello, World!");
})

application.listen(env.PORT || 80, () => {
    console.log(`Server is running on port ${env.PORT || 80}`);
});