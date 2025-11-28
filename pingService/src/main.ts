import express from "express"

const application = express();

application.get("/", (_, res) => {
    res.status(200).send("Hello, World!");
})

application.listen(80);