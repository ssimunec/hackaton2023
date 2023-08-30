const API_URL = 'http://192.168.100.63:8084';

export async function uploadImageApi(image: File, name: string) {
  const formData = new FormData();
  formData.append('file', image);
  formData.append('name', name);
  const response = await fetch(`${API_URL}/uploader`, {
    method: 'POST',

    body: formData,
  });
  return response.text();
}

export async function getDetectorApi(imageName: string) {
  const response = await fetch(`${API_URL}/detect`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image: imageName }),
  });
  const data: {position: number[]} = await response.json();
  return data.position;
}

export async function faceAnalyticsApi(imageName: string, position: number[]): Promise<{age: number, gender: string, sentiment: string}> {
  const response = await fetch(`${API_URL}/faceanalytics`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image: imageName, position }),
  });
  return response.json();
}

export async function recommendApi({age, gender, sentiment}: {age: number, gender: string, sentiment: string}) {
  const response = await fetch(`${API_URL}/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ age, gender, sentiment }),
  });
  const data: {recommend: string} = await response.json();
  return data.recommend;
}
