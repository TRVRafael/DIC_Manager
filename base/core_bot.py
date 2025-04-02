from importlib import import_module
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from base.handlers import verificar, apelidar, handle_new_user, handle_user_removed, oficializar, force_members_message_update, kick, remover_apelido
from base.handlers.funcoes_command_handler import editar_permissoes, mudar_permissao, funcoes, exibir_permissoes_funcao, finalizar
from base.handlers.list_command_handler import log_role, log_lideres

class CoreBot:
    def __init__(self, div_shortname: str):
        self.div = div_shortname
        self.token = self._get_bot_token()
        self.app = None # Será criado no start()
        self.roles = {
            "membros": 0,
            "auxiliares": 1,
            "core": 5,
            "comando": 6,
            "comandogeral": 7,
            "presidencia": 8,
        }      
        
    def _get_bot_token(self) -> str:
        """Obtém o token com tratamento de erros detalhado"""
        from base.config import BOT_TOKENS
        
        try:
            return BOT_TOKENS[self.div]
        except KeyError:
            available = list(BOT_TOKENS.keys())
            raise ValueError(
                f"Divisão '{self.div}' não encontrada. Divisões disponíveis: {available}"
            ) from None
        except AttributeError:
            raise AttributeError("BOT_TOKENS não está definido corretamente em base.config") from None
              
    def _wrap_handler(self, handler, *args, **kwargs):
        def wrapped(update, context):
            context.bot_data['div'] = self.div
            return handler(update, context, *args, **kwargs)
        return wrapped
    
    def _wrap_callback(self, handler):
        def wrapped(update, context):
            if not hasattr(context, 'bot_data'):
                context.bot_data = {}
            context.bot_data['div'] = self.div
            
            query = update.callback_query
            context.bot_data['callback_data'] = query.data
            
            return handler(update, context)
        return wrapped
    
    def _register_handlers(self, app : Application):
        self.app.add_handler(CommandHandler("verificar", self._wrap_handler(verificar)))
        self.app.add_handler(CommandHandler("apelidar", self._wrap_handler(apelidar)))
        self.app.add_handler(CommandHandler("oficializar", self._wrap_handler(oficializar)))
        self.app.add_handler(CommandHandler("force_update", self._wrap_handler(force_members_message_update)))
        self.app.add_handler(CommandHandler("kick", self._wrap_handler(kick)))
        self.app.add_handler(CommandHandler("remover_apelido", self._wrap_handler(remover_apelido)))

        self.app.add_handler(CommandHandler("lideranca", self._wrap_handler(log_lideres)))
        for command, role_id in self.roles.items():
            wrapped_handler = self._wrap_handler(
                lambda update, context, role_id=role_id: log_role(update, context, role_id)
            )
            self.app.add_handler(CommandHandler(command, wrapped_handler))

        self.app.add_handler(CommandHandler("funcoes", self._wrap_handler(funcoes)))
        self.app.add_handler(CallbackQueryHandler(editar_permissoes, pattern='^editar_permissoes$'))
        self.app.add_handler(CallbackQueryHandler(finalizar, pattern='^finalizar$'))
        
        for i in range(1, 7):
            # Handler para editar permissões
            callback_func = lambda update, context, i=i: exibir_permissoes_funcao(
                update, 
                context,
                f'editar_{i}'
            )
            
            self.app.add_handler(
                CallbackQueryHandler(
                    self._wrap_callback(callback_func),
                    pattern=f'^editar_{i}$'
                )
            )

        for i in range(1, 7):
            # Handler para mudar permissões
            callback_func = lambda update, context, i=i: mudar_permissao(
                update,
                context,
                f'permissao_{i}'
            )
            
            self.app.add_handler(
                CallbackQueryHandler(
                    self._wrap_callback(callback_func),
                    pattern=f'^permissao_{i}$'
                )
            )
        
        self.app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_user))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_user_removed))
        
    def start(self):
        self.app = Application.builder().token(self.token).build()
        self._register_handlers(self.app)
        print(f"Bot '{self.div}' rodando.")
        self.app.run_polling()