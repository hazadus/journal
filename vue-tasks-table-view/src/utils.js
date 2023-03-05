export function useFormatDateTime(dateIsoFormatString) {
  // Format date like "06.02.2023 20:05" from python `date.isoformat` string.
  let date = new Date(dateIsoFormatString);
  return date.toLocaleDateString("ru-RU") + " " + date.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit"
  });
}

export function useAuthorAvatarURL(entity) {
  // Returns URL of `entity` author. Entity must be either a comment or a task.
  // If there's no URL, a link to default profile pic will be returned.
  if (entity.author_avatar_url) {
    return '/media/' + entity.author_avatar_url;
  } else {
    return '/static/images/default_profile_pic.png';
  }
}

export function useAuthorShortName(entity) {
  // Returns author's name in "Иванов И.И." format
  // `entity` must be either a comment or a task.
  return `${entity.author_last_name} ${entity.author_first_name.slice(0, 1)}.${entity.author_second_name.slice(0, 1)}.`;
}

export function useLinesCount(text) {
  // Returns number of lines in `text`
  return typeof text == 'string' ? text.split(/\r\n|\r|\n/).length : 0;
}