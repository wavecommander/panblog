// Fuck JavaScript

const DATE_STR_LEN = 10;
const _MS_PER_DAY = 1000 * 60 * 60 * 24;

// https://stackoverflow.com/a/15289883/7789162
function dateDiffInDays(a, b) {
  const utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
  const utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());

  return Math.floor((utc2 - utc1) / _MS_PER_DAY);
}

headers = document.getElementsByTagName("h3")
for(let header of headers) {
    let innerHTML = header.nextElementSibling.innerHTML;
    let postTitle = innerHTML.substring(0, innerHTML.length - DATE_STR_LEN);

    let postDate = new Date(innerHTML.substring(innerHTML.length - DATE_STR_LEN));
    let numDays = dateDiffInDays(postDate, new Date());

    let fullText = postTitle;

    if(numDays == 0) {
      fullText += "today";
    } else if(numDays == 1) {
      fullText += "yesterday";
    } else {
      fullText += numDays + " days ago";
    }

    header.nextElementSibling.innerHTML = fullText;
}
