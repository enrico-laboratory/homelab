# Proxmox Full-Clone
# ---
# Create a new VM from a clone

resource "proxmox_vm_qemu" "test_vm" {

  # VM General Settings
  target_node = "node01"
  vmid = "199"
  name = "test-vm"
  desc = "Description"

  # VM Advanced General Settings
  onboot = true

  # VM OS Settings
  clone = "ubuntu-server-focal"

  # VM System Settings
  agent = 1

  # VM CPU Settings
  cores = 2
  sockets = 1
  cpu = "host"

  # VM Memory Settings
  memory = 2048

  # VM Network Settings
  network {
    bridge = "vmbr0"
    model  = "virtio"
  }

  network {
    bridge = "vmbr1"
    model  = "virtio"
  }

  # VM Cloud-Init Settings
  os_type = "cloud-init"

  # IP Address and Gateway
   ipconfig0 = "ip=192.168.2.51/24,gw=12.168.2.254"
   ipconfig2 = "ip=192.168.100.13/24"
#   Default User
   ciuser = "eruggieri"

  # (Optional) Add your SSH KEY
   sshkeys = <<EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC1LPH4xdHwaiyljtGmbh8muR848PKM8bxwuHkOPX0wFsXgP2m6bP2tZJrDOo42lTp7UEJ348R1YAX8h2HMNWpi87K9Eh8marRqS3Q4lMz7NWsveWN2CCT8VPBtDq+HiQWaEEOEB0O09yXQzY0MsuJ/7TLkT+gunfAugd36Dii/FQWc7dx9TMryFIGYh8GqlfDHT4s3KGUfanuRRO7HTLEVaN0L8iSF3R2hT3rsN3L9t501gcAMf8RwnCaVL3xTx4UZBbrx2Wa2w0EMskgV5XIacIAidjCeQM9/5VtDpXuD1tTryMPgreKVKq521BbYNxjJhBUwqGeyRrZTr4Ov1ca1vDa+KqsDARfYrYczcfgqS43MUOd322gPHjjr32l3/nycA2CTc98RNQSbLjW/GLhoua1GRnStKaOiYpKfu1LdHZIZ21hbQITx++RyaXQ0c1RCaAvTHbnxWrXe9kaL0ix/+cXcp2J1SNoICDdkPS+xtordxN55TqBKoqbK2lhMOds= eruggieri@NL-K4VLK9VG3Q
   EOF
}