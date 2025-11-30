// 初始化空的题库结构
const emptyBanks = {};

localStorage.setItem('questionBanks', JSON.stringify(emptyBanks));
localStorage.removeItem('currentBank');

console.log('题库已初始化为空');
