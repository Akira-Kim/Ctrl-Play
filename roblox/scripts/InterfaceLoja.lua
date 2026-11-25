
-- Interface da loja de itens

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local jogador = Players.LocalPlayer
local eventoCompra = ReplicatedStorage:WaitForChild("ComprarItem")

local gui = script.Parent
gui.ResetOnSpawn = false

-- Criar elementos visuais
local function criarElemento(tipo, propriedades, pai)
	local elemento = Instance.new(tipo)

	for propriedade, valor in pairs(propriedades) do
		elemento[propriedade] = valor
	end

	elemento.Parent = pai
	return elemento
end

local function arredondar(elemento)
	criarElemento("UICorner", {
		CornerRadius = UDim.new(0, 12)
	}, elemento)
end

-- Botão para abrir a loja
local botaoAbrir = criarElemento("TextButton", {
	Name = "AbrirLoja",
	Size = UDim2.fromOffset(130, 45),
	Position = UDim2.new(0, 20, 0.5, -22),
	BackgroundColor3 = Color3.fromRGB(35, 145, 90),
	Text = "LOJA",
	TextColor3 = Color3.new(1, 1, 1),
	TextSize = 22,
	Font = Enum.Font.GothamBold
}, gui)

arredondar(botaoAbrir)

-- Janela principal
local janela = criarElemento("Frame", {
	Name = "JanelaLoja",
	Size = UDim2.fromOffset(420, 390),
	Position = UDim2.new(0.5, -210, 0.5, -195),
	BackgroundColor3 = Color3.fromRGB(35, 39, 52),
	Visible = false
}, gui)

arredondar(janela)

-- Título
criarElemento("TextLabel", {
	Size = UDim2.new(1, -65, 0, 55),
	Position = UDim2.fromOffset(15, 5),
	BackgroundTransparency = 1,
	Text = "LOJA DE ITENS",
	TextColor3 = Color3.new(1, 1, 1),
	TextSize = 25,
	Font = Enum.Font.GothamBold,
	TextXAlignment = Enum.TextXAlignment.Left
}, janela)

-- Botão fechar
local botaoFechar = criarElemento("TextButton", {
	Size = UDim2.fromOffset(40, 40),
	Position = UDim2.new(1, -48, 0, 8),
	BackgroundColor3 = Color3.fromRGB(180, 55, 55),
	Text = "X",
	TextColor3 = Color3.new(1, 1, 1),
	TextSize = 22,
	Font = Enum.Font.GothamBold
}, janela)

arredondar(botaoFechar)

-- Área dos produtos
local lista = criarElemento("Frame", {
	Size = UDim2.new(1, -30, 0, 235),
	Position = UDim2.fromOffset(15, 65),
	BackgroundTransparency = 1
}, janela)

criarElemento("UIListLayout", {
	Padding = UDim.new(0, 10),
	SortOrder = Enum.SortOrder.LayoutOrder
}, lista)

-- Mensagem de compra
local mensagem = criarElemento("TextLabel", {
	Size = UDim2.new(1, -30, 0, 55),
	Position = UDim2.fromOffset(15, 310),
	BackgroundTransparency = 1,
	Text = "Escolha um item para comprar!",
	TextColor3 = Color3.fromRGB(230, 230, 230),
	TextSize = 15,
	Font = Enum.Font.Gotham,
	TextWrapped = true
}, janela)

-- Produtos e preços
local produtos = {
	{nome = "SpeedCoil", preco = 2, titulo = "Speed Coil"},
	{nome = "Gravity Coil", preco = 5, titulo = "Gravity Coil"},
	{nome = "Rainbow Magic Carpet", preco = 10, titulo = "Rainbow Magic Carpet"}
}

local botoes = {}
local comprados = {}
local comprando = false

for ordem, produto in ipairs(produtos) do

	local cartao = criarElemento("Frame", {
		Size = UDim2.new(1, 0, 0, 65),
		BackgroundColor3 = Color3.fromRGB(55, 62, 80),
		LayoutOrder = ordem
	}, lista)

	arredondar(cartao)

	criarElemento("TextLabel", {
		Size = UDim2.new(0.58, 0, 1, 0),
		Position = UDim2.fromOffset(12, 0),
		BackgroundTransparency = 1,
		Text = produto.titulo .. "\n" .. produto.preco .. " moedas",
		TextColor3 = Color3.new(1, 1, 1),
		TextSize = 16,
		Font = Enum.Font.GothamBold,
		TextXAlignment = Enum.TextXAlignment.Left
	}, cartao)

	local botao = criarElemento("TextButton", {
		Size = UDim2.fromOffset(115, 42),
		Position = UDim2.new(1, -125, 0.5, -21),
		BackgroundColor3 = Color3.fromRGB(35, 145, 90),
		Text = "COMPRAR",
		TextColor3 = Color3.new(1, 1, 1),
		TextSize = 15,
		Font = Enum.Font.GothamBold
	}, cartao)

	arredondar(botao)

	botoes[produto.nome] = botao

	botao.MouseButton1Click:Connect(function()

		if comprando or comprados[produto.nome] then
			return
		end

		comprando = true
		mensagem.Text = "Processando compra..."

		local sucesso, resultado, resposta = pcall(function()
			return eventoCompra:InvokeServer(produto.nome)
		end)

		if not sucesso then
			mensagem.Text = "Erro ao comunicar com a loja."
		elseif resultado then
			comprados[produto.nome] = true
			botao.Text = "COMPRADO"
			botao.BackgroundColor3 = Color3.fromRGB(90, 90, 90)
			mensagem.Text = resposta
		else
			mensagem.Text = resposta or "Não foi possível comprar."
		end

		comprando = false
	end)
end

-- Abrir e fechar
botaoAbrir.MouseButton1Click:Connect(function()
	janela.Visible = true
end)

botaoFechar.MouseButton1Click:Connect(function()
	janela.Visible = false
end)
