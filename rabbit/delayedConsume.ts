import { connect, credentials } from "amqplib";

const connection = await connect("amqp://51.250.26.59", { credentials: credentials.amqplain("guest", "guest123") })
const channel = await connection.createChannel();

await channel.assertQueue("IKBO-32-22_Vokhrin", { durable: false, autoDelete: false });

channel.consume("IKBO-32-22_Vokhrin", (msg) => {
    console.log(` [x] Received: "${msg?.content.toString()}"`);
    setTimeout(() => {
        channel.ack(msg!);
        console.log(" [x] Done");
    }, Number(msg?.content.toString()) * 1000);
}, { noAck: false });