
local CollectionService = game:GetService("CollectionService")

-- Configurações da esteira
local VELOCIDADE_PADRAO = 10
local TAG_ESTEIRA = "Conveyor"

-- Configura o funcionamento de uma esteira
local function configurarEsteira(esteira)

	-- Verifica se o objeto é uma peça
	if not esteira:IsA("BasePart") then
		return
	end

	-- Define a velocidade da esteira
	local velocidade = esteira:GetAttribute("Speed") or VELOCIDADE_PADRAO

	esteira.Anchored = true
	esteira.AssemblyLinearVelocity =
		esteira.CFrame:VectorToWorldSpace(Vector3.zAxis * -velocidade)

	-- Esconde o indicador de direção, se existir
	local indicador = esteira:FindFirstChildWhichIsA("SurfaceGui")

	if indicador then
		indicador.Enabled = false
	end
end

-- Configura todas as esteiras existentes
for _, esteira in CollectionService:GetTagged(TAG_ESTEIRA) do
	configurarEsteira(esteira)
end

-- Configura automaticamente as novas esteiras
CollectionService:GetInstanceAddedSignal(TAG_ESTEIRA):Connect(configurarEsteira)
