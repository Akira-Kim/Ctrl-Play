
	-- =========================================
	-- CONFIGURAÇÕES DO JOGADOR
	-- Altere os valores abaixo para personalizar
	-- o personagem durante a partida.
	-- =========================================

	local CONFIG = {

		-- Velocidade de caminhada
		Velocidade = 16,

		-- Força do pulo
		ForcaDoPulo = 50,

		-- Vida máxima do jogador
		VidaMaxima = 100,

		-- Vida inicial do jogador
		VidaInicial = 100,

	}

	-- =========================================
	-- APLICAÇÃO DAS CONFIGURAÇÕES
	-- Não é necessário modificar esta parte.
	-- =========================================

	local Players = game:GetService("Players")

	local function configurarJogador(personagem)

		local humanoide = personagem:WaitForChild("Humanoid")

		-- Movimento
		humanoide.WalkSpeed = CONFIG.Velocidade

		-- Pulo
		humanoide.UseJumpPower = true
		humanoide.JumpPower = CONFIG.ForcaDoPulo

		-- Vida
		humanoide.MaxHealth = CONFIG.VidaMaxima
		humanoide.Health = CONFIG.VidaInicial

	end

	local function iniciarJogador(jogador)

		jogador.CharacterAdded:Connect(configurarJogador)

		if jogador.Character then
			configurarJogador(jogador.Character)
		end

	end

	-- Jogadores que já estão na partida
	for _, jogador in ipairs(Players:GetPlayers()) do
		iniciarJogador(jogador)
	end

	-- Novos jogadores
	Players.PlayerAdded:Connect(iniciarJogador)
	world!")
