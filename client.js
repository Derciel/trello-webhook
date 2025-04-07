const t = TrelloPowerUp.iframe();

const gerarId = () => 'PU-' + Math.random().toString(36).substr(2, 6).toUpperCase();

document.getElementById('gerar-id').addEventListener('click', async () => {
  const idGerado = gerarId();

  // Obtém os campos personalizados do board
  const customFields = await t.get('board', 'shared', 'customFields') || [];

  // Procura o campo personalizado com nome "ID Power-Up"
  const campoIdPowerUp = customFields.find(field => field.name === 'ID Power-Up');

  if (!campoIdPowerUp) {
    alert('Campo personalizado "ID Power-Up" não encontrado.');
    return;
  }

  // Salva o ID no campo personalizado do card
  await t.set('card', 'shared', {
    [`customField_${campoIdPowerUp.id}`]: idGerado
  });

  alert(`ID salvo: ${idGerado}`);
});
