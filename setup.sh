#!/bin/bash
# Pensare OS — Setup completo
# Execute: bash setup.sh

set -e

ROOT="/Users/alicycarvalho/pensare-os"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════╗"
echo "║         PENSARE OS — SETUP            ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# 1. Dependências do dashboard
echo -e "${YELLOW}[1/4] Instalando dependências do dashboard...${NC}"
cd "$ROOT/dashboard"
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Dashboard pronto${NC}"

# 2. Permissões dos scripts
echo -e "${YELLOW}[2/4] Configurando permissões...${NC}"
chmod +x "$ROOT/.claude/skills/_shared/bin/"*
chmod +x "$ROOT/heartbeat/daemon.py"
chmod +x "$ROOT/heartbeat/install.sh"
echo -e "${GREEN}✓ Scripts executáveis${NC}"

# 3. PATH dos bin scripts
echo -e "${YELLOW}[3/4] Configurando PATH...${NC}"
BIN_PATH="$ROOT/.claude/skills/_shared/bin"
SHELL_RC="$HOME/.zshrc"
[ -f "$HOME/.bashrc" ] && SHELL_RC="$HOME/.bashrc"

if ! grep -q "pensare-os" "$SHELL_RC" 2>/dev/null; then
  echo "" >> "$SHELL_RC"
  echo "# Pensare OS bin scripts" >> "$SHELL_RC"
  echo "export PATH=\"$BIN_PATH:\$PATH\"" >> "$SHELL_RC"
  echo -e "${GREEN}✓ PATH adicionado em $SHELL_RC${NC}"
else
  echo -e "${GREEN}✓ PATH já configurado${NC}"
fi

# 4. Heartbeat (opcional)
echo -e "${YELLOW}[4/4] Heartbeat daemon...${NC}"
read -p "   Instalar heartbeat automático? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
  bash "$ROOT/heartbeat/install.sh"
  echo -e "${GREEN}✓ Heartbeat instalado${NC}"
else
  echo "   Pulado — rode manualmente: python $ROOT/heartbeat/daemon.py --once"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         SETUP CONCLUÍDO ✓             ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════╝${NC}"
echo ""
echo "Como usar:"
echo ""
echo "  1. DASHBOARD WEB:"
echo "     cd $ROOT/dashboard && python server.py"
echo "     → http://localhost:8360"
echo ""
echo "  2. AGENTES (Claude Code):"
echo "     cd $ROOT && claude"
echo "     > /pensare [seu objetivo aqui]"
echo ""
echo "  3. HEARTBEAT MANUAL:"
echo "     python $ROOT/heartbeat/daemon.py --dry-run   (preview)"
echo "     python $ROOT/heartbeat/daemon.py --once      (roda agora)"
echo "     python $ROOT/heartbeat/daemon.py             (daemon contínuo)"
echo ""
echo "  4. VERIFICAR STATUS:"
echo "     pensare-status"
echo "     pensare-cost --alert"
echo ""
echo "  Próximo passo: preencha _contexto/empresa.md com os dados do seu negócio."
echo ""
