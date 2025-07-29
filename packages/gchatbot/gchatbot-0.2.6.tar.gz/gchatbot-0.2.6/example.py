# main.py
import os
import time
import asyncio
from typing import Any, Dict
from fastapi import FastAPI, Request
from gchatbot import GChatBot, ExtractedEventData, EventPayload, ProgressiveResponse, ResponseType

# Certifique-se de ter um arquivo 'service.json' ou defina a variável de ambiente.
SERVICE_ACCOUNT_FILE: str = os.environ.get("SERVICE_ACCOUNT_FILE", "service.json")

class BotExemplo(GChatBot):
    """
    Bot de exemplo que demonstra métodos síncronos e assíncronos.
    
    Este exemplo mostra como você pode misturar métodos sync e async
    na mesma classe, e a biblioteca automaticamente detecta e trata
    cada um de forma apropriada.
    
    Também demonstra respostas progressivas (progressive fallback).
    """
    def __init__(self) -> None:
        super().__init__(
            botName="Bot Exemplo Híbrido",
            serviceAccountFile=SERVICE_ACCOUNT_FILE,
            syncTimeout=4.0  # Responde em até 4s ou muda para modo assíncrono.
        )

    async def _processSlashCommand(self, command: str, arguments: str, extractedData: ExtractedEventData, eventData: EventPayload) -> ResponseType:
        """
        MÉTODO ASSÍNCRONO - Processa comandos de barra usando async/await.
        
        Este método é async, então pode usar await para operações não-bloqueantes.
        
        Args:
            command: Nome do comando sem a barra (/)
            arguments: Argumentos passados após o comando
            extractedData: Dados estruturados extraídos do evento
            eventData: Payload original do evento do Google Chat
            
        Returns:
            str: Resposta simples
            OU Tuple[str, Callable]: Resposta progressiva (rápida + detalhada)
        """
        user: str = extractedData.get('userDisplayName', 'Usuário')
        userChatId: str = extractedData.get('userGoogleChatId', 'Unknown ID')
        
        if command == "lento":
            # Operação assíncrona que demora mais que o syncTimeout
            await asyncio.sleep(6)
            return f"⏱️ Comando /lento ASYNC executado para {user} (ID: {userChatId})! Demorou 6 segundos de forma não-bloqueante."
        
        elif command == "rapido":
            # Operação assíncrona rápida
            await asyncio.sleep(1)
            return f"⚡ Comando /rapido ASYNC executado rapidamente para {user}!"
        
        elif command == "api":
            # Simula chamada para API externa assíncrona
            await asyncio.sleep(3)
            return f"🌐 Chamada ASYNC para API externa concluída para {user}!"
        
        elif command == "concorrente":
            # Demonstra operações concorrentes
            tasks: list[asyncio.Task[str]] = [
                asyncio.create_task(self._operacaoAsync(f"Task {i}", 1)) 
                for i in range(3)
            ]
            resultados: list[str] = await asyncio.gather(*tasks)
            return f"🚀 Operações concorrentes para {user}:\n" + "\n".join(resultados)
        
        elif command == "progressivo":
            # 🆕 Demonstra resposta progressiva ASSÍNCRONA
            quickResponse = f"⚡ Iniciando análise para {user}..."
            
            async def detailedResponse() -> str:
                await asyncio.sleep(5)  # Simula processamento longo
                dados = await self._analisarDadosAsync()
                return f"📊 Análise completa para {user}!\n\nResultados:\n{dados}"
            
            return (quickResponse, detailedResponse)
        
        elif command == "relatorio":
            # 🆕 Demonstra resposta progressiva com processamento complexo
            quickResponse = f"📋 Gerando relatório para {user}..."
            
            async def detailedResponse() -> str:
                # Simula várias etapas de processamento
                await asyncio.sleep(2)  # Coleta de dados
                await asyncio.sleep(3)  # Processamento
                await asyncio.sleep(2)  # Formatação
                return f"✅ Relatório completo gerado para {user}!\n\n📈 Dados processados\n📊 Gráficos gerados\n📄 Documento finalizado"
            
            return (quickResponse, detailedResponse)
        
        elif command == "info":
            # 🆕 Demonstra uso do userGoogleChatId
            userEmail: str = extractedData.get('userEmail', 'Unknown Email')
            spaceName: str = extractedData.get('spaceName', 'Unknown Space')
            isDM: bool = extractedData.get('isDirectMessageEvent', False)
            
            return f"""ℹ️ **Informações do Usuário e Contexto:**

👤 **Usuário:**
• Nome: {user}
• Email: {userEmail}
• Google Chat ID: {userChatId}

🏠 **Espaço:**
• Nome: {spaceName}
• Tipo: {'Mensagem Direta (DM)' if isDM else 'Sala/Grupo'}

💡 **Dica:** O Google Chat ID é útil para menções programáticas e identificação única!"""
        
        else:
            await asyncio.sleep(0.5)
            return f"✅ Comando ASYNC /{command} executado para {user}."

    def _processMessage(self, text: str, extractedData: ExtractedEventData, eventData: EventPayload) -> ResponseType:
        """
        MÉTODO SÍNCRONO - Processa mensagens usando métodos tradicionais.
        
        Este método é síncrono (sem async), então usa time.sleep() e 
        operações bloqueantes normais.
        
        Args:
            text: Texto processado da mensagem
            extractedData: Dados estruturados extraídos do evento
            eventData: Payload original do evento do Google Chat
            
        Returns:
            str: Resposta simples
            OU Tuple[str, Callable]: Resposta progressiva (rápida + detalhada)
        """
        user: str = extractedData.get('userDisplayName', 'Usuário')
        userChatId: str = extractedData.get('userGoogleChatId', 'Unknown ID')
        
        if "demorado" in text.lower():
            # Operação síncrona que bloqueia a thread
            time.sleep(7)
            return f"🕐 Você pediu algo demorado, {user} (ID: {userChatId}). Processamento SÍNCRONO concluído em 7 segundos!"
        
        elif "progressivo" in text.lower():
            # 🆕 Demonstra resposta progressiva SÍNCRONA
            quickResponse = f"⚡ Recebido! Processando sua solicitação, {user}..."
            
            def detailedResponse() -> str:
                time.sleep(4)  # Simula processamento
                resultado = self._processarDadosSync()
                return f"📋 Análise completa concluída para {user}!\n\nResultados: {resultado}"
            
            return (quickResponse, detailedResponse)
        
        elif "analise" in text.lower():
            # 🆕 Outro exemplo de resposta progressiva síncrona
            quickResponse = f"🔍 Iniciando análise para {user}..."
            
            def detailedResponse() -> str:
                time.sleep(3)  # Processamento
                return f"📊 Análise detalhada concluída para {user}!\n\n✅ Dados validados\n📈 Tendências identificadas\n🎯 Recomendações geradas"
            
            return (quickResponse, detailedResponse)
        
        elif "meusdados" in text.lower():
            # 🆕 Demonstra acesso aos dados do usuário incluindo o Google Chat ID
            userEmail: str = extractedData.get('userEmail', 'Unknown Email')
            spaceName: str = extractedData.get('spaceName', 'Unknown Space')
            isDM: bool = extractedData.get('isDirectMessageEvent', False)
            
            return f"""📋 **Seus Dados:**

👤 **Identificação:**
• Nome: {user}
• Email: {userEmail}
• Google Chat ID: {userChatId}

🏠 **Contexto Atual:**
• Espaço: {spaceName}
• Tipo: {'Mensagem Direta' if isDM else 'Sala/Grupo'}

🔍 **Texto Original:** "{extractedData.get('rawText', 'N/A')}"
📝 **Texto Processado:** "{extractedData.get('processedText', 'N/A')}"

💡 O Google Chat ID é único e pode ser usado para menções programáticas!"""
        
        elif "calcular" in text.lower():
            # Processamento síncrono intensivo
            time.sleep(2)
            resultado: int = sum(range(1000000))
            return f"🧮 Cálculo SÍNCRONO concluído para {user}: {resultado}"
        
        elif "processar" in text.lower():
            # Simula processamento de dados síncrono
            time.sleep(3)
            return f"📊 Dados processados de forma SÍNCRONA para {user}!"
        
        elif "sync" in text.lower():
            # Operação síncrona rápida
            time.sleep(1)
            return f"⚡ Processamento SÍNCRONO rápido para {user}!"
        
        else:
            # Mensagem padrão síncrona
            return f"💬 Mensagem processada de forma SÍNCRONA, {user}: '{text}'"

    # --- Métodos auxiliares assíncronos ---
    
    async def _operacaoAsync(self, nome: str, duracao: int) -> str:
        """Método auxiliar assíncrono."""
        await asyncio.sleep(duracao)
        return f"✓ {nome} concluída ASYNC em {duracao}s"
    
    async def _analisarDadosAsync(self) -> str:
        """Simula análise de dados assíncrona."""
        await asyncio.sleep(2)
        return "• Padrões identificados\n• Anomalias detectadas\n• Relatório gerado"
    
    def _processarDadosSync(self) -> str:
        """Simula processamento de dados síncrono."""
        time.sleep(2)
        return "Dados processados com sucesso"

# --- Configuração do FastAPI ---
app: FastAPI = FastAPI(title="Google Chat Bot - Exemplo Híbrido")
bot: BotExemplo = BotExemplo()

@app.post("/google-chat-webhook")
async def handleEvent(request: Request) -> Any:
    """
    Ponto de entrada para todos os eventos do Google Chat.
    
    Args:
        request: Requisição HTTP do FastAPI contendo o payload do evento
        
    Returns:
        Resposta JSON para o Google Chat
    """
    return await bot.handleRequest(request)

@app.get("/")
def home() -> Dict[str, Any]:
    """
    Endpoint para verificação de saúde.
    
    Returns:
        Dicionário com informações sobre o bot e exemplos de uso
    """
    return {
        "status": "ativo", 
        "bot_name": bot.botName, 
        "hybrid_support": True,
        "comandos_async": [
            "/lento - Operação assíncrona longa (6s)",
            "/rapido - Operação assíncrona rápida (1s)", 
            "/api - Simula chamada API assíncrona (3s)",
            "/concorrente - Operações paralelas assíncronas",
            "/progressivo - 🆕 Resposta progressiva async: rápida + detalhada",
            "/relatorio - 🆕 Resposta progressiva async com múltiplas etapas",
            "/info - 🆕 Mostra informações do usuário incluindo Google Chat ID"
        ],
        "mensagens_sync": [
            "Envie 'demorado' para teste síncrono longo (7s)",
            "Envie 'calcular' para cálculo síncrono (2s)",
            "Envie 'processar' para processamento síncrono (3s)",
            "Envie 'sync' para teste síncrono rápido (1s)",
            "Envie 'progressivo' - 🆕 Resposta progressiva sync",
            "Envie 'analise' - 🆕 Resposta progressiva sync detalhada",
            "Envie 'meusdados' - 🆕 Mostra seus dados incluindo Google Chat ID"
        ],
        "observacao": "Comandos de barra são ASYNC, mensagens normais são SYNC",
        "nova_funcionalidade": "🆕 Respostas Progressivas: Resposta rápida imediata + atualização detalhada automática"
    }

@app.get("/test")
def testEndpoint() -> Dict[str, Any]:
    """
    Endpoint de teste.
    
    Returns:
        Dicionário com informações sobre o status do servidor
    """
    return {
        "message": "Servidor funcionando!", 
        "slash_commands": "async",
        "messages": "sync",
        "hybrid_mode": True,
        "progressive_responses": True
    }

# Para executar localmente: uvicorn example:app --reload --port 8080