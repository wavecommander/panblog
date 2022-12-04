// Fuck JavaScript

const DATE_STR_LEN = 10;
const _MS_PER_DAY = 1000 * 60 * 60 * 24;

headers = document.getElementsByTagName("h3");
for (let header of headers) {
  let innerHTML = header.nextElementSibling.innerHTML;
  let postTitle = innerHTML.substring(0, innerHTML.length - DATE_STR_LEN);

  let postDate = new Date(innerHTML.substring(innerHTML.length - DATE_STR_LEN));
  let numDays = Math.floor((new Date() - postDate) / _MS_PER_DAY);

  let fullText = postTitle;

  if (numDays == 0) {
    fullText += "today";
  } else if (numDays == 1) {
    fullText += "yesterday";
  } else {
    fullText += numDays + " days ago";
  }

  header.nextElementSibling.innerHTML = fullText;
}
