// 设置测试题库数据到localStorage
const testBank = {
  "默认题库": [
    {
      "hint": "你好吗？",
      "correctSentence": "How are you?"
    },
    {
      "hint": "我很好，谢谢。",
      "correctSentence": "I am fine, thank you."
    }
  ]
};

localStorage.setItem('questionBanks', JSON.stringify(testBank));
localStorage.setItem('currentBank', '默认题库');

console.log('测试题库已设置到localStorage');