// bot.js
const venom = require('venom-bot');
const axios = require('axios');

// URL da sua API Python
const API_URL = 'http://localhost:5000/mensagem';

function log(msg) {
    console.log(`[BOT] ${msg}`);
}

venom
    .create({
        session: 'nutribot-session', // nome da sessão
    })
    .then((client) => start(client))
    .catch((err) => {
        console.error('Erro ao iniciar venom:', err);
    });

function start(client) {
    log('Bot iniciado. Escaneie o QR Code no terminal se aparecer.');

    client.onMessage(async (message) => {
        try {
            // ignora grupos, se quiser
            if (message.isGroupMsg) return;

            const from = message.from;    // ID do usuário (telefone)
            const texto = message.body || '';

            // Opcional: comando rápido pra ajuda
            if (texto.toLowerCase().trim() === 'help') {
                await client.sendText(
                    from,
                    'Oi! Eu sou o NutriBot IA 🤖🥦.\n' +
                    'Envie qualquer mensagem para começar ou digite "novo" para reiniciar o plano.'
                );
                return;
            }

            // chama a API Python passando user_id + texto
            const resp = await axios.post(API_URL, {
                user_id: from,
                texto: texto
            });

            const respostaBot = resp.data.resposta || 'Erro inesperado ao processar a resposta.';

            // envia de volta pro WhatsApp
            await client.sendText(from, respostaBot);
            log(`Mensagem processada para ${from}`);

        } catch (err) {
            console.error('Erro ao tratar mensagem:', err);
            try {
                await client.sendText(
                    message.from,
                    'Ops, tive um problema técnico ao processar sua mensagem 😥\nTente novamente em alguns instantes.'
                );
            } catch (e2) {
                console.error('Erro ao enviar mensagem de erro:', e2);
            }
        }
    });
}
