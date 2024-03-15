// fetch("https://imdb8.p.rapidapi.com/auto-complete?q=game",
//   {"method": "GET",
//     "headers": {"X-rapidapi-host": "imdb8.p.rapidapi.com",
//       "X-rapidapi-key": "553339745emsh06fcd96c97f7e8cp122a89jsnfa2de77f963c"}})
// .then(response => response.json())
//   .then(data => {const list = data.d;
//
//     list.map((item) => {
//       const name = item.l;
//       const poster = item.i.imageUrl;
//       const movie = `<li><img src="${poster}"> <h2>${name}</h2></li>`;
//
//       document.querySelector('.movies').innerHTML += movie;
//     })
//   })
//   .catch(err => {
//     console.error(err);
// });
//
