
local Players = game:GetService("Players")
local CollectionService = game:GetService("CollectionService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Cria o evento para esconder moedas individualmente
local eventoEsconder = ReplicatedStorage:FindFirstChild("EsconderMoeda")

if not eventoEsconder then
	eventoEsconder = Instance.new("RemoteEvent")
	eventoEsconder.Name = "EsconderMoeda"
	eventoEsconder.Parent = ReplicatedStorage
end

-- Guarda quais moedas cada jogador já coletou
local moedasColetadas = {}

-- Configura uma moeda
local function configurarMoeda(moeda)

	if not moeda:IsA("BasePart") then
		return
	end

	-- Detecta quando alguém toca na moeda
	moeda.Touched:Connect(function(objeto)

		local personagem = objeto:FindFirstAncestorOfClass("Model")
		if not personagem then
			return
		end

		local jogador = Players:GetPlayerFromCharacter(personagem)
		if not jogador then
			return
		end

		-- Verifica se a moeda já foi coletada por esse jogador
		moedasColetadas[moeda] = moedasColetadas[moeda] or {}

		if moedasColetadas[moeda][jogador] then
			return
		end

		-- Verifica se o jogador está vivo
		local humanoide = personagem:FindFirstChildOfClass("Humanoid")

		if not humanoide or humanoide.Health <= 0 then
			return
		end

		-- Encontra o saldo do jogador
		local placar = jogador:FindFirstChild("leaderstats")
		local saldo = placar and placar:FindFirstChild("Moedas")

		if not saldo then
			return
		end

		-- Define o valor da moeda
		local valor = moeda:GetAttribute("Valor") or 1

		-- Adiciona as moedas ao jogador
		saldo.Value += valor

		-- Registra que esse jogador já coletou a moeda
		moedasColetadas[moeda][jogador] = true

		-- Esconde a moeda somente para quem coletou
		eventoEsconder:FireClient(jogador, moeda)

		print(jogador.Name, "coletou", valor, "moedas!")
	end)
end

-- Configura todas as moedas existentes
for _, moeda in CollectionService:GetTagged("Coin") do
	configurarMoeda(moeda)
end

-- Configura novas moedas adicionadas
CollectionService:GetInstanceAddedSignal("Coin"):Connect(configurarMoeda)

-- Limpa os dados quando o jogador sair
Players.PlayerRemoving:Connect(function(jogador)
	for _, jogadores in moedasColetadas do
		jogadores[jogador] = nil
	end
end)

