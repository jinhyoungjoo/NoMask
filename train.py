from importlib import import_module

import utils
from trainer.trainer import Trainer

packages = {
    "dataloader_module": import_module(".dataloader", "dataloader"),
    "model_module": import_module("model"),
    "loss_module": import_module("model", "losses"),
    "optimizer_module": import_module("torch.optim"),
    "lr_scheduler_module": import_module("torch.optim.lr_scheduler"),
}


def main(config):
    utils.set_seed(config["seed"])
    logger = config.get_logger("train")

    train_dataloader = config.build("train_dataloader", packages["dataloader_module"])

    validation_dataloader = config.build(
        "validation_dataloader", packages["dataloader_module"]
    )

    logger.info(f"Dataloader build success.")

    model = config.build("model", packages["model_module"])
    logger.info(f"Model build success.\n{model}")

    loss_function = config.build("loss", packages["loss_module"])
    logger.info("Loss build success.")

    optimizer = config.build(
        "optimizer", packages["optimizer_module"], model.parameters()
    )
    logger.info("Optimizer build success.")

    lr_scheduler = config.build(
        "lr_scheduler", packages["lr_scheduler_module"], optimizer
    )
    if lr_scheduler is not None:
        logger.info("LR scheduler build success.")

    logger.info("Start training...")

    trainer = Trainer(
        train_dataloader,
        validation_dataloader,
        model,
        loss_function,
        optimizer,
        lr_scheduler,
        config["trainer"],
        logger,
    )
    logger.info("Trainer build success.")

    trainer.train()
    logger.info("Start training...")


if __name__ == "__main__":
    config_file, args = utils.parse_argument()
    config = utils.ConfigParser(config_file, args)
    main(config)
