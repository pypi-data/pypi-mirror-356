use std::env;
use std::process;

mod cmds;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    // 跳过程序名称，获取命令参数
    let command_args = if args.len() > 1 {
        &args[1..]
    } else {
        &[]
    };
    
    // 使用共享的命令处理逻辑
    if let Err(e) = cmds::handle_command(command_args) {
        eprintln!("❌ Error: {}", e);
        process::exit(1);
    }
}