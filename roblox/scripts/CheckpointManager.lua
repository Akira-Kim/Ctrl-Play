
local Players = game:GetService("Players")
local CollectionService = game:GetService("CollectionService")

-- Guarda o último checkpoint de cada jogador
local checkpointsDosJogadores = {}

-- Teletransporta o jogador para seu último checkpoint

-- Teletransporta o jogador para seu último checkpoint
local function aoPersonagemNascer(personagem)

	local jogador = Players:GetPlayerFromCharacter(personagem)

	if not jogador then
		return
	end

	-- Espera o personagem carregar completamente
	local humanoide = personagem:WaitForChild("Humanoid")
	local parteCentral = personagem:WaitForChild("HumanoidRootPart")

	-- Aguarda um pequeno intervalo para terminar o carregamento
	task.wait(0.1)

	local checkpoint = checkpointsDosJogadores[jogador]

	if not checkpoint or not checkpoint.Parent then
		print("Nenhum checkpoint encontrado para:", jogador.Name)
		return
	end

	-- Calcula a altura necessária
	local altura = checkpoint.Size.Y / 2
		+ humanoide.HipHeight
		+ parteCentral.Size.Y / 2

	-- Define a posição de destino
	local destino = checkpoint.CFrame + Vector3.new(0, altura, 0)

	-- Teletransporta o jogador
	personagem:PivotTo(destino)

	print("Jogador retornou ao checkpoint:", checkpoint.Name)
end


-- Configura cada checkpoint
local function configurarCheckpoint(checkpoint)

	if not checkpoint:IsA("BasePart") then
		return
	end

	-- Detecta quando alguém toca no checkpoint
	checkpoint.Touched:Connect(function(objeto)

		print("Checkpoint tocado!")

		local personagem = objeto:FindFirstAncestorOfClass("Model")
		if not personagem then
			return
		end

		local jogador = Players:GetPlayerFromCharacter(personagem)
		if not jogador then
			return
		end

		local humanoide = personagem:FindFirstChildOfClass("Humanoid")

		if humanoide and humanoide.Health > 0 then

			-- Salva o checkpoint alcançado
			checkpointsDosJogadores[jogador] = checkpoint

			print("Checkpoint salvo para:", jogador.Name)
		end
	end)
end

-- Configura os jogadores
local function configurarJogador(jogador)

	jogador.CharacterAdded:Connect(aoPersonagemNascer)

	if jogador.Character then
		task.spawn(aoPersonagemNascer, jogador.Character)
	end
end

-- Configura jogadores existentes
for _, jogador in Players:GetPlayers() do
	configurarJogador(jogador)
end

-- Configura novos jogadores
Players.PlayerAdded:Connect(configurarJogador)

-- Apaga os dados quando o jogador sair
Players.PlayerRemoving:Connect(function(jogador)
	checkpointsDosJogadores[jogador] = nil
end)

-- Configura checkpoints existentes
for _, checkpoint in CollectionService:GetTagged("Checkpoint") do
	configurarCheckpoint(checkpoint)
end

-- Configura novos checkpoints
CollectionService:GetInstanceAddedSignal("Checkpoint"):Connect(configurarCheckpoint)
