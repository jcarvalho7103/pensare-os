#!/usr/bin/env bash
# heartbeat/install.sh — Instala o Pensare OS Heartbeat como LaunchAgent no macOS.
#
# O launchd chama daemon.py a cada 60 segundos (StartInterval).
# O script deve ser executado uma única vez por usuário.
#
# Para desinstalar (comentado abaixo):
#   launchctl unload ~/Library/LaunchAgents/com.pensareos.heartbeat.plist
#   rm ~/Library/LaunchAgents/com.pensareos.heartbeat.plist

set -euo pipefail

PLIST_LABEL="com.pensareos.heartbeat"
PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$PLIST_DIR/$PLIST_LABEL.plist"

BASE_DIR="/Users/alicycarvalho/pensare-os"
DAEMON_PY="$BASE_DIR/heartbeat/daemon.py"
LOG_OUT="$BASE_DIR/logs/heartbeat.stdout.log"
LOG_ERR="$BASE_DIR/logs/heartbeat.stderr.log"

# Garante que diretórios existem
mkdir -p "$PLIST_DIR"
mkdir -p "$BASE_DIR/logs"

# Resolve Python3 — preferência: python3 do sistema ou pyenv/homebrew
PYTHON_BIN=$(command -v python3 || echo "/usr/bin/python3")

echo "Instalando Pensare OS Heartbeat..."
echo "  Python:  $PYTHON_BIN"
echo "  Daemon:  $DAEMON_PY"
echo "  plist:   $PLIST_PATH"

# Escreve o plist
cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_BIN}</string>
        <string>${DAEMON_PY}</string>
        <string>--once</string>
    </array>

    <!-- Roda a cada 60 segundos -->
    <key>StartInterval</key>
    <integer>60</integer>

    <key>WorkingDirectory</key>
    <string>${BASE_DIR}</string>

    <key>StandardOutPath</key>
    <string>${LOG_OUT}</string>

    <key>StandardErrorPath</key>
    <string>${LOG_ERR}</string>

    <!-- Não inicia no boot sem login — só quando o usuário está logado -->
    <key>RunAtLoad</key>
    <true/>

    <!-- Reinicia se o processo sair com erro -->
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
PLIST

# Descarrega versão anterior se já estava instalada (ignora erro se não existia)
launchctl unload "$PLIST_PATH" 2>/dev/null || true

# Carrega o novo plist
launchctl load "$PLIST_PATH"

echo ""
echo "Heartbeat instalado e ativo."
echo ""
echo "Verificar status:   launchctl list $PLIST_LABEL"
echo "Ver log:            tail -f $LOG_OUT"
echo "Ver erros:          tail -f $LOG_ERR"
echo ""
echo "Para desinstalar:"
echo "  launchctl unload $PLIST_PATH"
echo "  rm $PLIST_PATH"
