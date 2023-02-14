# MIDI-OBS
Código para ativar o MUTE do canal 1 da FLOW 8 enviando um sinal MIDI quando uma cena em específico estiver ativa no OBS.

-- RESUMO

Este código é uma classe chamada Observer, que tem como objetivo monitorar a mudança de cena no OBS (Open Broadcasting Software)
e mudar o estado de um canal de um controlador MIDI baseado na cena atual.

A classe Observer inicializa um cliente de eventos do OBS e registra 
dois eventos para serem observados: on_current_program_scene_changed e on_exit_started. 
O primeiro evento é acionado quando a cena atual do programa muda e verifica se a cena atual é a 
desejada, que é carregada a partir de um arquivo config.toml. Se a cena desejada estiver ativa, o controlador MIDI é enviado 
um comando de mute ON. Caso contrário, o controlador é enviado um comando de mute OFF.

O segundo evento, on_exit_started, é acionado quando o OBS começa o processo de fechamento, mas atualmente não está sendo utilizado no código.

Por fim, existe um loop principal que mantém a classe Observer
funcionando enquanto a variável running for verdadeira. A cada iteração, o loop dorme por 1 segundo
