
-- Sistema de compras da loja

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")

local pastaDeItens = ServerStorage:WaitForChild("ItensDaLoja")

-- Preços dos itens
local precos = {
	["SpeedCoil"] = 2,
	["Gravity Coil"] = 5,
	["Rainbow Magic Carpet"] = 10
}

-- Jogadores que já compraram cada item
local comprasDosJogadores = {}

-- Criar comunicação com a interface
local eventoCompra = ReplicatedStorage:FindFirstChild("ComprarItem")

if not eventoCompra then
	eventoCompra = Instance.new("RemoteFunction")
	eventoCompra.Name = "ComprarItem"
	eventoCompra.Parent = ReplicatedStorage
end

-- Processar uma compra
eventoCompra.OnServerInvoke = function(jogador, nomeDoItem)

	-- Verificar se o item existe na lista
	local preco = precos[nomeDoItem]

	if not preco then
		return false, "Item inválido."
	end

	-- Verificar se o jogador já comprou
	comprasDosJogadores[jogador] = comprasDosJogadores[jogador] or {}

	if comprasDosJogadores[jogador][nomeDoItem] then
		return false, "Você já comprou esse item!"
	end

	-- Localizar as moedas do jogador
	local leaderstats = jogador:FindFirstChild("leaderstats")
	local moedas = leaderstats and leaderstats:FindFirstChild("Moedas")

	if not moedas then
		return false, "Não foi possível encontrar suas moedas."
	end

	-- Verificar saldo
	if moedas.Value < preco then
		return false, "Moedas insuficientes!"
	end

	-- Localizar a ferramenta
	local ferramenta = pastaDeItens:FindFirstChild(nomeDoItem)

	if not ferramenta or not ferramenta:IsA("Tool") then
		return false, "Ferramenta não encontrada."
	end

	-- Descontar moedas
	moedas.Value = moedas.Value - preco

	-- Entregar uma cópia para uso imediato
	local copia = ferramenta:Clone()
	copia.Parent = jogador:WaitForChild("Backpack")

	-- Guardar outra cópia para continuar disponível após morrer
	local copiaParaRespawn = ferramenta:Clone()
	copiaParaRespawn.Parent = jogador:WaitForChild("StarterGear")

	-- Registrar a compra
	comprasDosJogadores[jogador][nomeDoItem] = true

	return true, "Compra realizada com sucesso!"
end

-- Limpar dados quando o jogador sair
Players.PlayerRemoving:Connect(function(jogador)
	comprasDosJogadores[jogador] = nil
end)

