import time
import toml
import mido
from mido import Message

import obsws_python as obs

# Classe que monitora a mudança de cena no OBS e muda o estado do canal no controlador MIDI
class Observer:
    def __init__(self):
        # Inicializa o cliente de eventos do OBS
        self._client = obs.EventClient()
        # Registra os eventos que serão observados
        self._client.callback.register(
            [
                self.on_current_program_scene_changed,
                # self.on_exit_started,
            ]
        )
        # Exibe a lista de eventos registrados
        print(f"Registered events: {self._client.callback.get()}")
        # Variável que indica se o loop principal deve continuar rodando
        self.running = True
        # Variável que indica se a cena desejada está ativa
        self.sceneOn = False
        # Carrega a configuração da cena a ser monitorada a partir do arquivo config.toml
        with open("config.toml") as f:
            self.config = toml.load(f)

    def on_current_program_scene_changed(self, data):
        """The current program scene has changed."""
        # Exibe o nome da cena atual
        print(f"Switched to scene {data.scene_name}")

        # Verifica se está esperando a cena esperada
        if (data.scene_name == self.config['personal']['scene_name']):
            self.sceneOn = True
            try:
                # Abre a porta de saída MIDI
                with mido.open_output("FLOW 8 MIDI OUT 1") as output:
                    # Envia o comando de mute ON
                    cc_ONmute = Message('control_change', channel=0, control=5, value=1)
                    output.send(cc_ONmute)
                    print('mutado')
                # Fecha a porta de saída MIDI
                output.close()
            except Exception as e:
                print(f"Erro ao abrir porta de saida MIDI: {e}")
        elif self.sceneOn == True:
            self.sceneOn = False
            try:
                # Abre a porta de saída MIDI
                with mido.open_output("FLOW 8 MIDI OUT 1") as output:
                    # Envia o comando de mute OFF
                    cc_OFFmute = Message('control_change', channel=0, control=5, value=0)
                    output.send(cc_OFFmute)
                    print("desmutado")
                # Fecha a porta de saída MIDI
                output.close()
            except Exception as e:
                print(f"Erro ao abrir porta de saida MIDI: {e}")

    # def on_exit_started(self, _):
    #     """OBS has begun the shutdown process."""
    #     print(f"OBS closing!")
    #     self._client.unsubscribe()


if __name__ == "__main__":
    observer = Observer()

    while observer.running:
        time.sleep(1)
