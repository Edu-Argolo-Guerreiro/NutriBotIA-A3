// assets/chatbot/bot_wwjs.js
/**
 * Bot WhatsApp NutriBot IA
 * ------------------------
 *
 * Este script integra o NutriBot IA (API Flask em Python) com o WhatsApp
 * usando a biblioteca `whatsapp-web.js`.
 *
 * Fluxo:
 *  - O bot recebe mensagens no WhatsApp
 *  - Repassa o texto para a API Flask em /mensagem
 *  - Devolve a resposta do chatbot para o usuário
 *
 * Requisitos:
 *  - Node.js + npm
 *  - Dependências: whatsapp-web.js, qrcode-terminal, axios
 *  - API Flask do NutriBot rodando (por padrão em http://localhost:5000/mensagem)
 *
 * Observação:
 *  - A sessão do WhatsApp fica salva localmente via LocalAuth
 *    (não é necessário escanear o QR Code toda vez).
 *
 * Comentários e organização revisados com auxílio do ChatGPT (GPT-5.1 Thinking)
 * Data: 2025-11-19
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

// URL da API Flask que expõe a rota /mensagem
// Ajuste se a API estiver em outro host/porta.
const API_URL = 'http://localhost:5000/mensagem';

/**
 * Log helper com prefixo padrão do bot.
 */
function log(msg) {
    console.log('[BOT]', msg);
}

// ============================================================================
//  Configuração do cliente WhatsApp
// ============================================================================

const client = new Client({
    // LocalAuth salva a sessão em .wwebjs_auth (por cliente)
    authStrategy: new LocalAuth({ clientId: 'nutribot' }),
    puppeteer: {
        headless: false, // se quiser rodar "invisível" em produção, troque para true
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--disable-gpu',
        ],
    },
});

// ============================================================================
//  Eventos de sessão / conexão
// ============================================================================

// Exibe QR Code no terminal para parear o WhatsApp
client.on('qr', (qr) => {
    console.log('QR CODE GERADO, aponte a câmera do celular 👇');
    qrcode.generate(qr, { small: true });
});

// Quando estiver pronto para uso
client.on('ready', () => {
    console.log('✅ WhatsApp Web pronto! Pode mandar mensagem para o número do bot.');
});

// Autenticação bem sucedida
client.on('authenticated', () => {
    console.log('🔐 Autenticado com sucesso.');
});

// Falha de autenticação
client.on('auth_failure', (msg) => {
    console.error('❌ Falha na autenticação:', msg);
});

// Desconectado do WhatsApp
client.on('disconnected', (reason) => {
    console.log('📴 Desconectado do WhatsApp:', reason);
});

// ============================================================================
//  Handler principal de mensagens recebidas
// ============================================================================

client.on('message', async (msg) => {
    console.log('--- Mensagem recebida ---');
    console.log({
        from: msg.from,
        body: msg.body,
        isGroupMsg: msg.from.endsWith('@g.us'),
        type: msg.type,
    });
    console.log('-------------------------');

    // Ignora mensagens de grupos (apenas privado)
    if (msg.from.endsWith('@g.us')) return;

    const texto = (msg.body || '').trim();
    const from = msg.from;

    if (!texto) return;

    // ------------------------------------------------------------------------
    // Comandos simples locais (não chamam a API Flask)
    // ------------------------------------------------------------------------
    if (['oi', 'olá', 'ola', 'menu'].includes(texto.toLowerCase())) {
        await client.sendMessage(
            from,
            'Olá! Eu sou o NutriBot IA 🤖🥦\n' +
            'Envie *plano* para começar a montar seu plano alimentar.'
        );
        return;
    }

    if (texto.toLowerCase() === 'ping') {
        await client.sendMessage(from, 'pong ✅');
        return;
    }

    // ------------------------------------------------------------------------
    // Comando para iniciar o fluxo de plano alimentar
    // ------------------------------------------------------------------------
    if (texto.toLowerCase() === 'plano') {
        // Envia a mensagem "novo" para a API, o que faz o chatbot reiniciar o fluxo
        try {
            const resp = await axios.post(API_URL, {
                user_id: from, // usamos o número do WhatsApp como identificador de usuário
                texto: 'novo',
            });

            const respostaBot =
                resp.data?.resposta ||
                'Erro inesperado ao iniciar o plano. Tente novamente.';

            await client.sendMessage(from, respostaBot);
            log(`Fluxo iniciado para ${from}`);
        } catch (err) {
            console.error('Erro ao chamar API /mensagem (novo):', err.message);
            await client.sendMessage(
                from,
                'Tive um erro técnico ao iniciar seu plano 😥\nTente novamente em alguns instantes.'
            );
        }
        return;
    }

    // ------------------------------------------------------------------------
    // Qualquer outra mensagem é repassada para o chatbot Python (API Flask)
    // ------------------------------------------------------------------------
    try {
        const resp = await axios.post(API_URL, {
            user_id: from, // mantém o estado por usuário no backend
            texto: texto,
        });

        const respostaBot =
            resp.data?.resposta || 'Erro inesperado ao processar sua mensagem.';

        await client.sendMessage(from, respostaBot);
        log(`Mensagem processada para ${from}`);
    } catch (err) {
        console.error('Erro ao chamar API /mensagem:', err.message);
        await client.sendMessage(
            from,
            'Ops, tive um problema técnico ao falar com o NutriBot 😥\n' +
            'Tente novamente em alguns instantes.'
        );
    }
});

// ============================================================================
//  Inicialização do cliente
// ============================================================================

client.initialize();
