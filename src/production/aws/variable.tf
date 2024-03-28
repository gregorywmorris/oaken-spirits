variable "environment" {
  type = string
  default = "development"
}

variable "instance_metadata_options" {
  description = "Metadata options for EC2 instance"
  type = object({
    http_endpoint               = string
    http_tokens                 = string
    http_put_response_hop_limit = number
  })
  default = {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
}