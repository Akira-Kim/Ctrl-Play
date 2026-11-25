
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Recebe o aviso de moeda coletada
local eventoEsconder = ReplicatedStorage:WaitForChild("EsconderMoeda")

-- Esconde a moeda somente para esse jogador
eventoEsconder.OnClientEvent:Connect(function(moeda)

	if moeda and moeda:IsA("BasePart") then
		moeda.LocalTransparencyModifier = 1
	end
end)

