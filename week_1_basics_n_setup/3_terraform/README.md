Ôn tập terraform

1. Đầu tiền tạo service account, set quyển basic owner (chỉ dùng cho develop, production tìm hiểu sau)
2. Tạo key và copy vào thư mục /.google/credentials (thư mục quản lý key của gcp), tự định nghĩa
3. tạo một thư mục mới, tạo file main.tf
4. set up provider

```bash
provider "google" {
    project = "savvy-octagon-362900"
    region = "asia-northeast1"
    credentials = "~/.google/credentials/terraform.json"
}
```

5 terraform init

Ví dụ: Provisioning Google Compute Engine Instance

1. Cấp phép sử dụng Compute Engine API trên GCP (enable API) thông qua search
2. Viết code, có thể tham khảo ở đây: https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started, https://viblo.asia/p/nhap-mon-infrastructure-as-code-su-dung-terraform-de-provision-infrastructure-tren-gcp-m68Z0PoAZkG

3. terraform plan (kiểm tra xem có vấn đề gì không)
4. enable Identity and Access Management (IAM) API
5. terraform apply (deploy infras lên gcp)
6. muốn check xem nginx đã chạy chưa làm theo https://www.youtube.com/watch?v=GTCxNJhVxEc

- sudo apt-get update
- sudo apt-get install nginx
- sudo apt-get install ufw
- sudo ufw allow 'Nginx HTTP'
- systemctl status nginx
  nhớ set allow http traffic, https traffic thì mới kết nối vs nginx đc

7. terraform destroy
   terraform destroy -auto-approve
